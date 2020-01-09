
title: "Custom sklearn transformer"
date: 2019-12-28  
disqus: false
draft: true

Scikit-learn comes with a handful of useful built-in data transformation functions that allow you to fill in missing values, scale numerical data, etc. Eventually, however, you will want manipulate your data in a way that is not supported by the built-in offerings. Fortunately, it's not too hard to construct your own transformer that can easily be integrated with the greater sklearn workflow.

For this exercise, I'm going to be using data about my Spotify Discover Weekly playlists. If you don't know about [Discover Weekly](https://hackernoon.com/spotifys-discover-weekly-how-machine-learning-finds-your-new-music-19a41ab76efe) (who are you?!), you'll probably want to acquaint yourself. I've been collecting data on my weekly playlists since fall of 2019 with vague plans to turn it into some sort of project. The [spotipy](https://spotipy.readthedocs.io/en/latest/) library makes it easy to access all of the amazing data that Spotify makes available through its API.


```python
import pandas as pd
import pathlib

project_dir = pathlib.Path().cwd().parent
df = pd.read_pickle(project_dir / 'data/raw/dw_combined.pkl')

cols = ['song_length_ms', 'popularity', 'tempo', 'danceability', 'energy']
df = df[cols]
df.head()
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
      <th>popularity</th>
      <th>tempo</th>
      <th>danceability</th>
      <th>energy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>217131</td>
      <td>35</td>
      <td>151.858</td>
      <td>0.553</td>
      <td>0.281</td>
    </tr>
    <tr>
      <th>1</th>
      <td>255800</td>
      <td>38</td>
      <td>125.580</td>
      <td>0.421</td>
      <td>0.374</td>
    </tr>
    <tr>
      <th>2</th>
      <td>188000</td>
      <td>28</td>
      <td>127.380</td>
      <td>0.512</td>
      <td>0.205</td>
    </tr>
    <tr>
      <th>3</th>
      <td>448349</td>
      <td>36</td>
      <td>146.544</td>
      <td>0.286</td>
      <td>0.506</td>
    </tr>
    <tr>
      <th>4</th>
      <td>291080</td>
      <td>37</td>
      <td>80.059</td>
      <td>0.491</td>
      <td>0.262</td>
    </tr>
  </tbody>
</table>
</div>



The above code loads the Discover Weekly data and selects the columns that we will use to build our custom transformer.


```python

```
