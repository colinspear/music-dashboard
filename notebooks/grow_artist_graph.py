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
artists
# %%
seed = 'Bonnie Prince Billy'

# 1. Create seed artist's related artist graph
# 2. Calculate and record average path length and clustering coefficient
# 3. Get related artists for all of artists in graph created in Step 1.
# 4. Create graph of this 