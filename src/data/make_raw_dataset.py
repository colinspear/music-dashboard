import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from pathlib import Path

import discover_weekly as dw

print('Downloading Discover Weekly song data...')
today = datetime.today().strftime('%Y-%m-%d')
pickle_str = ('data/raw/discover_weekly/' + today + '-discover-weekly.pkl')
pickle_path = Path(__file__).resolve().parent.parent.parent / pickle_str

# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()

# load up the entries as environment variables
load_dotenv(dotenv_path)

username = 'colinspear1'
scope = 'user-library-read'
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
redirect_uri = os.environ.get("REDIRECT_URI")

all_tracks = dw.collect_and_append_new_dw(
    username,
    client_id,
    client_secret,
    redirect_uri,
    scope
)

all_tracks.to_pickle(pickle_path)

print('Download complete!')
