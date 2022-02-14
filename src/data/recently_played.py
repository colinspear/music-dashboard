import os
import pickle
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

import spotipy
from spotipy.oauth2 import SpotifyOAuth

data_dir = Path('../../data/raw/recently_played')

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

with open('after.pkl', 'wb') as h:
    after = pickle.load(h)

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
redirect_uri = os.environ.get("REDIRECT_URI")
# username = 'colinspear1'
scope = 'user-read-recently-played' #, 'user-read-playback-position', 'user-read-playback-state', 'user-read-currently-playing', 'user-library-read']


sp = spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        client_id = client_id,
        client_secret = client_secret,
        redirect_uri = redirect_uri,
        scope = scope
        )
    )

data = sp.current_user_recently_played()
with open('data.pkl', 'wb') as h:
    pickle.dump(data, h, protocol=pickle.HIGHEST_PROTOCOL)

after = data['cursors']['after']

with open('after.pkl', 'wb') as h:
    pickle.dump(after, h, protocol=pickle.HIGHEST_PROTOCOL)

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
