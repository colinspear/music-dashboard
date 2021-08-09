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
# I think this looks like a Small world network. Check properties to see how well it conforms or not

# create a graph from the full artist sample
G = nx.from_pandas_edgelist(
    r, 
    source='artist',
    target='related_artist',
    # edge_attr='followers',
    # create_using=nx.DiGraph()
)

# calculate clustering coefficient
c = nx.average_clustering(G)

# the full graph is not actually connected. In order to calculate shortest
# path, we need a connected graph. There are twelve sub-graphs, one of which
# is much larger than the others. I will just use the largest subgraph

l = nx.average_shortest_path_length(G)
# %%
for i, C in enumerate((G.subgraph(c).copy() for c in nx.connected_components(G))):
    print(i, nx.average_shortest_path_length(C))
# %%
# so there is actually a built in function to test small-worldness in NetworkX.
# It might be fun to do the calculation myself and compare it to the results of
# built in. The built in is making my machine work... (didn't finish)
# nx.sigma(G)
# nx.omega(G)
# %%
largest_cc = max(nx.connected_components(G), key=len)
S = G.subgraph(largest_cc)
# %%
print(G.number_of_nodes())
print(S.number_of_nodes())
# %%
R = nx.random_reference(S)
# %%
L = nx.lattice_reference(S)
# %%

l = nx.average_shortest_path_length(S)
l_r = nx.average_shortest_path_length(R)
l_l = nx.average_shortest_path_length(L)
# %%
c = nx.average_clustering(S)
c_r = nx.average_clustering(R)
c_l = nx.average_clustering(L)

# %%
s = (c / c_r) / (l / l_r)
s
# %%
o = (l_r / l) - (c / c_l)
o
# %%
swi = ((l - l_l) / (l_r - l_l)) / ((c - c_r) / (c_l - c_r))
swi
# %%
s2 = nx.sigma(S)
# %%
o2 = nx.omega(S)
# %%
