---
title: "Custom sklearn transformer"
date: 2019-12-28  
disqus: false
draft: true
---
Scikit-learn comes with a number of useful built-in data transformation functions that allow you to [impute missing values](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.impute), [scale numerical data](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.preprocessing), etc. Eventually, however, you will want to manipulate your data in a way that is not supported by the built-in offerings. Fortunately, it's not too hard to construct your own transformer that can easily be integrated with the greater sklearn workflow.

Scikit-learn is an incredibly powerful data processing and machine learning library straight out of the box. 
The majority of tasks most people will want to do are supported by their built in methods, which is great. 
However, there will inevitably come a day when you want to do something that is not possible straight out of the box.
Fortunately, sklearn is also incredibly [well designed](https://arxiv.org/abs/1309.0238) and makes creating your own methods and integrating them into your workflow super straightforward.

## How the sausage gets made

- Include a brief intro to sklearn's API design

For this exercise, I'm going to be using data about my Spotify Discover Weekly playlists. 
If you don't know about [Discover Weekly](https://hackernoon.com/spotifys-discover-weekly-how-machine-learning-finds-your-new-music-19a41ab76efe) (who are you?!), you'll probably want to acquaint yourself. 
I've been collecting data on my weekly playlists since fall of 2019 with vague plans to turn it into some sort of project. 
The [spotipy](https://spotipy.readthedocs.io/en/latest/) library makes it easy to access all of the amazing data that Spotify makes available through its API.


```python
import pandas as pd
import pathlib

project_dir = pathlib.Path().cwd().parent
song_features = pd.read_pickle(project_dir / 'data/raw/dw_combined.pkl')

cols = ['song_length_ms', 'tempo', 'tempo_confidence',
        'instrumentalness', 'liveness', 'loudness', 'speechiness', 
        'valence', 'acousticness', 'danceability', 
        'energy', 'popularity']

song_features = song_features[cols]
```

```python
song_features.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>song_length_ms</th>
      <th>tempo</th>
      <th>tempo_confidence</th>
      <th>instrumentalness</th>
      <th>liveness</th>
      <th>loudness</th>
      <th>speechiness</th>
      <th>valence</th>
      <th>acousticness</th>
      <th>danceability</th>
      <th>energy</th>
      <th>popularity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>217131</td>
      <td>151.858</td>
      <td>0.094</td>
      <td>0.0205</td>
      <td>0.3230</td>
      <td>-13.417</td>
      <td>0.0555</td>
      <td>0.501</td>
      <td>0.976</td>
      <td>0.553</td>
      <td>0.281</td>
      <td>35</td>
    </tr>
    <tr>
      <th>1</th>
      <td>255800</td>
      <td>125.580</td>
      <td>0.361</td>
      <td>0.0309</td>
      <td>0.1420</td>
      <td>-12.015</td>
      <td>0.0306</td>
      <td>0.218</td>
      <td>0.938</td>
      <td>0.421</td>
      <td>0.374</td>
      <td>38</td>
    </tr>
    <tr>
      <th>2</th>
      <td>188000</td>
      <td>127.380</td>
      <td>0.231</td>
      <td>0.0158</td>
      <td>0.2580</td>
      <td>-14.418</td>
      <td>0.0500</td>
      <td>0.296</td>
      <td>0.791</td>
      <td>0.512</td>
      <td>0.205</td>
      <td>28</td>
    </tr>
    <tr>
      <th>3</th>
      <td>448349</td>
      <td>146.544</td>
      <td>0.046</td>
      <td>0.1210</td>
      <td>0.9460</td>
      <td>-11.329</td>
      <td>0.0637</td>
      <td>0.268</td>
      <td>0.902</td>
      <td>0.286</td>
      <td>0.506</td>
      <td>36</td>
    </tr>
    <tr>
      <th>4</th>
      <td>291080</td>
      <td>80.059</td>
      <td>0.126</td>
      <td>0.0062</td>
      <td>0.0878</td>
      <td>-12.572</td>
      <td>0.0316</td>
      <td>0.334</td>
      <td>0.849</td>
      <td>0.491</td>
      <td>0.262</td>
      <td>37</td>
    </tr>
  </tbody>
</table>
</div>



Generally, when we want to make a custom transformer, we should have some reason to believe that a specific combination or transformation of one or more variables will be a good predictor for the target variable. We don't have a super obvious such relationship here, so I'm going to make some hypotheses without any evidence in their favor. Don't do this in the wild. 

My first hypothesis is that faster soongs will be more popular. But I want to adjust for uncertainty in song speed. To do this I can use `tempo_confidence` to weight `tempo`, essentially "slowing down" tracks that have lower degree of tempo certainty.

The second hypothesis is a bit more far-fetched, so I am only going to include it as an optional argument in my transformer. I'm going to say more danceable songs will be more popular, so long as they are not too long (people get tired, right?). So if we divide `song_length_ms` by `danceability`, the resulting feature (`fatigue_factor`) should have an inverse relationship with popularity. We can alway see if this brazen assumption holds after we make the transformation.

```python
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

# get the right column indices: safer than hard-coding indices 3, 4, 5, 6
tempo_ix, tempo_conf_ix, dance_ix, length_ix = [
    list(song_features.columns).index(col)
    for col in ('tempo', 'tempo_confidence', 'danceability', 'song_length_ms')]

class CustomFeaturesAdder(BaseEstimator, TransformerMixin):
    def __init__(self, add_fatigue_factor = True): # no *args or **kwargs
        self.add_fatigue_factor = add_fatigue_factor
    def fit(self, X, y=None):
        return self  # nothing else to do
    def transform(self, X, y=None):
        weighted_tempo = X[:, tempo_ix] * X[:, tempo_conf_ix]
        if self.add_fatigue_factor:
            fatigue_factor = X[:, length_ix] / X[:, dance_ix]
            return np.c_[X, weighted_tempo, fatigue_factor]
        else:
            return np.c_[X, weighted_tempo]

features_adder = CustomFeaturesAdder(add_fatigue_factor=True)
music_plus = features_adder.transform(song_features.values)
```

```python
pd.DataFrame(music_plus).head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>10</th>
      <th>11</th>
      <th>12</th>
      <th>13</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>217131.0</td>
      <td>151.858</td>
      <td>0.094</td>
      <td>0.0205</td>
      <td>0.3230</td>
      <td>-13.417</td>
      <td>0.0555</td>
      <td>0.501</td>
      <td>0.976</td>
      <td>0.553</td>
      <td>0.281</td>
      <td>35.0</td>
      <td>14.274652</td>
      <td>3.926420e+05</td>
    </tr>
    <tr>
      <th>1</th>
      <td>255800.0</td>
      <td>125.580</td>
      <td>0.361</td>
      <td>0.0309</td>
      <td>0.1420</td>
      <td>-12.015</td>
      <td>0.0306</td>
      <td>0.218</td>
      <td>0.938</td>
      <td>0.421</td>
      <td>0.374</td>
      <td>38.0</td>
      <td>45.334380</td>
      <td>6.076010e+05</td>
    </tr>
    <tr>
      <th>2</th>
      <td>188000.0</td>
      <td>127.380</td>
      <td>0.231</td>
      <td>0.0158</td>
      <td>0.2580</td>
      <td>-14.418</td>
      <td>0.0500</td>
      <td>0.296</td>
      <td>0.791</td>
      <td>0.512</td>
      <td>0.205</td>
      <td>28.0</td>
      <td>29.424780</td>
      <td>3.671875e+05</td>
    </tr>
    <tr>
      <th>3</th>
      <td>448349.0</td>
      <td>146.544</td>
      <td>0.046</td>
      <td>0.1210</td>
      <td>0.9460</td>
      <td>-11.329</td>
      <td>0.0637</td>
      <td>0.268</td>
      <td>0.902</td>
      <td>0.286</td>
      <td>0.506</td>
      <td>36.0</td>
      <td>6.741024</td>
      <td>1.567654e+06</td>
    </tr>
    <tr>
      <th>4</th>
      <td>291080.0</td>
      <td>80.059</td>
      <td>0.126</td>
      <td>0.0062</td>
      <td>0.0878</td>
      <td>-12.572</td>
      <td>0.0316</td>
      <td>0.334</td>
      <td>0.849</td>
      <td>0.491</td>
      <td>0.262</td>
      <td>37.0</td>
      <td>10.087434</td>
      <td>5.928310e+05</td>
    </tr>
  </tbody>
</table>
</div>


