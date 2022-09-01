#!/usr/bin/env python3

# %%

from pathlib import Path

import pandas as pd

project_path = Path("..")
latest_rp = sorted(project_path.glob("data/processed/2*recently_played_tracks.csv"))[-1]
# %% 

df = pd.read_csv(latest_rp)
# %%

top_artists = df.groupby('artist_name')["artist_name"].count().sort_values(ascending=False)
top_artists.head(20)
# %%

df.columns


# %%
df.info()
# %%
