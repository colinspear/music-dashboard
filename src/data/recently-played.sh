#!/usr/bin/env sh

# curl -X "GET" -G \
#     "https://api.spotify.com/v1/me/player/recently-played" \
    # -d before=1644625561389 \
#     -d limit=50 \
#     -H "Accept: application/json" \
#     -H "Content-Type: application/json" \
#     -H "Authorization: Bearer 

source .env-bash

curl -X "GET" -G \
    "https://api.spotify.com/v1/me/player/recently-played?before=1644625561389" \
    -d limit=50 \
    -d client_id=$CLIENT_ID \
    -d client_secret=$CLIENT_SECRET \
    -d response_type='code'
    -d redirect_uri=$REDIRECT_URI \
    -d scope='user-read-recently-played' \
    -H "Accept: application/json" \
    -H "Content-Type: application/json"
    # -H "Authorization: Bearer
