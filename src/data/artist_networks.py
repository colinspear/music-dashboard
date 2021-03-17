import os
import requests
import json

from dotenv import load_dotenv, find_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials


# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()
# load up the entries as environment variables
load_dotenv(dotenv_path)

username = 'colinspear1'
scope = 'user-follow-read'
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
redirect_uri = os.environ.get("REDIRECT_URI")


def instantiate_client(username, client_id, client_secret, redirect_uri, scope):
    sp = spotipy.Spotify(
        auth_manager = SpotifyOAuth(
            client_id = client_id,
            client_secret = client_secret,
            redirect_uri = redirect_uri,
            scope = scope
            )
        )

    return sp

def followed_artists():
    sp = instantiate_client(username, client_id, client_secret, redirect_uri, scope='user-follow-read')
    artists = []
    follow = sp.current_user_followed_artists(limit=50, after=None)
    while len(follow['artists']['items']) > 0:
        artists = artists + follow['artists']['items']
        last_artist_id = follow['artists']['items'][-1]['id']
        follow = sp.current_user_followed_artists(limit=50, after=last_artist_id)
    
    return artists

def related_artists():
    sp = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
    )
    artist_list = followed_artists()
    for i in range(len(artist_list)):
        related_resp = sp.artist_related_artists(artist_list[i]['uri'])
        artist_list[i]['related_artists'] = [i['name'] for i in related_resp['artists']]
        artist_list[i]['related_ids'] = [i['id'] for i in related_resp['artists']]

    return artist_list


with open('data/raw/followed_artists.json', 'w') as fp:
    json.dump(related_artists(), fp, sort_keys=True, indent=4)

