#!/usr/bin/env python3

import pickle
from pathlib import Path
from datetime import date

import pandas as pd

project_path = Path("../..")
rp_files = (project_path / "data/raw/recently_played").glob("2*.pkl")
tracks = []

for f in rp_files:
    with open(f, 'rb') as p:
        d = pickle.load(p)
    
    try:
        for i in d['items']:
            played_at = i['played_at']
            track_id = i['track']['id']
            track_name = i['track']['name']
            album_id = i['track']['album']['id']
            album_name = i['track']['album']['name']
            release_date = i['track']['album']['release_date']
            release_date_precision = i['track']['album']['release_date_precision']
            duration_ms = i['track']['duration_ms']
            track_popularity = i['track']['popularity']
            artists = i['track']['artists']

            for a in artists:
                artist_id = a['id']
                artist_name = a['name']

                track = (
                    played_at, track_id, track_name, artist_id, artist_name, album_id, album_name, 
                    release_date, release_date_precision, duration_ms, track_popularity
                )

                tracks.append(track)
    except TypeError:
        print("The following file had issues:\n\n", f)
        pass

columns = ("played_at", "track_id", "track_name", "artist_id", "artist_name", "album_id", "album_name", 
    "release_date", "release_date_precision", "duration_ms", "track_popularity")

df = pd.DataFrame.from_records(tracks, columns=columns)
today = date.today().strftime('%Y-%m-%d')
df.to_csv(project_path / f"data/processed/{today}_recently_played_tracks.csv", index=False)

