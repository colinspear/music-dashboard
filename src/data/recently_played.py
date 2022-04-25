import os
import pickle
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from datetime import datetime

import spotipy
from spotipy.oauth2 import SpotifyOAuth

data_dir = Path('../../data/raw/recently_played')

now = datetime.now().strftime('%Y-%m-%d-%H%M%S')
log_now = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

print(f'{log_now} : start download')

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

try:
    with open(data_dir / 'after.pkl', 'rb') as h:
        after = pickle.load(h)
except FileNotFoundError:
    print(f'Could not find {data_dir}. Proceeding without after timestamp')

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
redirect_uri = os.environ.get("REDIRECT_URI")
username = 'colinspear1'
scope = 'user-read-recently-played' #, 'user-read-playback-position', 'user-read-playback-state', 'user-read-currently-playing', 'user-library-read']

sp = spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        # username=username,
        client_id = client_id,
        client_secret = client_secret,
        redirect_uri = redirect_uri,
        scope = scope
        )
    )

try:
    data = sp.current_user_recently_played(after=after)
except NameError:
    print('No after date found. Proceeding without after timestamp.')
    data = sp.current_user_recently_played()

n = len(data['items'])

try:
    after = data['cursors']['after']
except TypeError:
    print(f'{log_now} : {n} songs downloaded. Next download will start after {after}') 

if n > 0: 
    with open(data_dir / f'{now}-recently_played.pkl', 'wb') as h:
        pickle.dump(data, h)

    with open(data_dir / 'after.pkl', 'wb') as h:
        pickle.dump(after, h)
    print(f'{log_now} : {n} songs downloaded. Next download will start after {after}')


# FAILED REQUESTS ATTEMPT

# import requests
# from requests_oauthlib import OAuth2Session
# from requests.auth import HTTPBasicAuth


# request_url = "https://accounts.spotify.com/authorize" #"https://api.spotify.com/v1/me/player/recently-played"
# token_url = "https://accounts.spotify.com/api/token"
# # response_type = 'code'

# oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
# authorization_url, state = oauth.authorization_url(request_url)

# print(f'Please go to {authorization_url} and authorize access.')

# authorization_response = input('Enter the full callback URL')

# token = oauth.fetch_token(
#         'https://accounts.google.com/o/oauth2/token',
#         authorization_response=authorization_response,
#         # Google specific extra parameter used for client
#         # authentication
#         client_secret=client_secret)

# r = oauth.get('https://www.googleapis.com/oauth2/v1/userinfo')
