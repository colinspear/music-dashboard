# %%
import json

import networkx as nx
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# %%
with open('../data/raw/followed_artists.json') as f:
    artists = json.load(f)
# %%
artists_dict = {}
artists_dict['id'] = [i['id'] for i in artists]
artists_dict['artist'] = [i['name'] for i in artists]
artists_dict['followers'] = [i['followers']['total'] for i in artists]
artists_dict['popularity'] = [i['popularity'] for i in artists]
# artists_dict['image_url'] =  [i['images'][0]['url'] for i in artists]
artists_dict['related_artist'] = [i['related_artists'] for i in artists]
# artists_dict['related_id'] = [i['related_ids'] for i in artists]
# %%
df = pd.DataFrame.from_dict(artists_dict)
# %%
# "melt" name list into individual rows
# https://stackoverflow.com/questions/27263805/pandas-column-of-lists-create-a-row-for-each-list-element

lst_col = 'related_artist'

r = pd.DataFrame({
      col:np.repeat(df[col].values, df[lst_col].str.len())
      for col in df.columns.drop(lst_col)}
    ).assign(**{lst_col:np.concatenate(df[lst_col].values)})[df.columns]
# %%
# temp fix to remove special characters from name (Joey Bada$$ was throwing an error)
r['artist'] = r['artist'].str.replace('$', 'S')
r['related_artist'] = r['related_artist'].str.replace('$', 'S')
# %%
r.loc[r['related_artist'].str.contains('\$')]
# %%
r_graph = r.sample(500)
G = nx.from_pandas_edgelist(r_graph, 
                            source='artist',
                            target='related_artist',
                            # edge_attr='followers',
                            create_using=nx.DiGraph())
# %%
nx.draw_networkx(G, with_labels=False, node_size=10, width=0.5)
# %%
