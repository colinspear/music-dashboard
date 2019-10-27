# a program to download a current discover weekly playlist
# and save to disk

# import required modules
import sys
import spotipy
import spotipy.util as util
import pandas as pd


def track_info_df(sp, song_list):
    """
    Takes a list of dictionaries returned from spotipy json
    responses and creates a pandas data frame of its
    characteristics

    :song_list: list of dictionaries of track characteristics
    """
    # initiate song dictionary
    song_dict = dict(
        time_added=[],
        release_date=[],
        release_date_precision=[],
        artist_name=[],
        artist_id=[],
        song_id=[],
        song_length_ms=[],
        song_name=[],
        popularity=[],
        loudness = [],
        tempo = [],
        tempo_confidence = [],
        time_signature = [],
        time_sig_conf = [],
        key = [],
        key_confidence = [],
        mode = [],
        mode_confidence = [],
        danceability = [],
        energy = [],
        speechiness = [],
        acousticness = [],
        instrumentalness = [],
        liveness = [],
        valence = [],
    )

    # collect saved track data
    for i, song in enumerate(song_list):
        if song_list[i]['track']['id'] in song_dict['song_id']:
            continue
        else:
            song_dict['time_added'].append(song_list[i]['added_at'])
            song_dict['release_date'].append(song_list[i]['track']['album']['release_date'])
            song_dict['release_date_precision'].append(song_list[i]['track']['album']['release_date_precision'])
            song_dict['artist_name'].append(song_list[i]['track']['album']['artists'][0]['name'])
            song_dict['artist_id'].append(song_list[i]['track']['artists'][0]['id'])
            song_dict['song_id'].append(song_list[i]['track']['id'])
            song_dict['song_length_ms'].append(song_list[i]['track']['duration_ms'])
            song_dict['song_name'].append(song_list[i]['track']['name'])
            song_dict['popularity'].append(song_list[i]['track']['popularity'])

            audio_analysis = sp.audio_analysis(song_list[i]['track']['id'])
            song_dict['loudness'].append(audio_analysis['track']['loudness'])
            song_dict['tempo'].append(audio_analysis['track']['tempo'])
            song_dict['tempo_confidence'].append(audio_analysis['track']['tempo_confidence'])
            song_dict['time_signature'].append(audio_analysis['track']['time_signature'])
            song_dict['time_sig_conf'].append(audio_analysis['track']['time_signature_confidence'])
            song_dict['key'].append(audio_analysis['track']['key'])
            song_dict['key_confidence'].append(audio_analysis['track']['key_confidence'])
            song_dict['mode'].append(audio_analysis['track']['mode'])
            song_dict['mode_confidence'].append(audio_analysis['track']['mode_confidence'])

            audio_features = sp.audio_features(song_list[i]['track']['id'])
            song_dict['danceability'].append(audio_features[0]['danceability'])
            song_dict['energy'].append(audio_features[0]['energy'])
            song_dict['speechiness'].append(audio_features[0]['speechiness'])
            song_dict['acousticness'].append(audio_features[0]['acousticness'])
            song_dict['instrumentalness'].append(audio_features[0]['instrumentalness'])
            song_dict['liveness'].append(audio_features[0]['liveness'])
            song_dict['valence'].append(audio_features[0]['valence'])

    fave_songs = pd.DataFrame(song_dict)
    return fave_songs
    #fave_songs.to_pickle('starred_songs.pkl')

def discover_weekly_track_list(sp, username):
    """Returns list of Discover Weekly song
    characteristics

    :session: authorized spotipy instance
    """
    offset = 0
    playlists = []
    dw_tracks = []
    while offset < 100:
        playlists.append(sp.user_playlists(username, offset=offset))
        offset += 50

    for i in playlists:
        for pl in i['items']:
            name = pl['name']
            if name == 'Discover Weekly':
                playlist_id = pl['id']
                dw_tracks = sp.user_playlist_tracks(username, playlist_id=playlist_id)
            else:
                continue

    return dw_tracks['items']

def collect_and_append_new_dw(username,
                             client_id,
                             client_secret,
                             redirect_uri,
                             scope):
    """Collects current Discover Weekly track information
    and appends to previously existing track info
    """

    token = util.prompt_for_user_token(
    username=username,
    scope=scope,
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri
    )

    # instantiate spotipy
    sp = spotipy.Spotify(auth=token)

    current_tracks = discover_weekly_track_list(sp, username)
    current_tracks_df = track_info_df(sp, current_tracks)

    return current_tracks_df
