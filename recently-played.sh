# curl -X "GET" -G \
#     "https://api.spotify.com/v1/me/player/recently-played" \
    # -d before=1644625561389 \
#     -d limit=50 \
#     -H "Accept: application/json" \
#     -H "Content-Type: application/json" \
#     -H "Authorization: Bearer BQDKzXRxdVdB5WWfZZvJI5VxwHkgb_uSyb4T2oJ8iL4VwAETZLCOSup7zMFdXE2QBiocdCK01kWhIOF056aE7c1-U8SLFIXvpYoF3hqjTZNpYL6c8rpWPfy1Y8m_e7rijhpDHVaf3z8IU8hlmfwR_QupIvh0oqpsO44rS2PG"

curl -X "GET" -G \
    "https://api.spotify.com/v1/me/player/recently-played?before=1644625561389" \
    -d limit=50 \
    -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer BQDKzXRxdVdB5WWfZZvJI5VxwHkgb_uSyb4T2oJ8iL4VwAETZLCOSup7zMFdXE2QBiocdCK01kWhIOF056aE7c1-U8SLFIXvpYoF3hqjTZNpYL6c8rpWPfy1Y8m_e7rijhpDHVaf3z8IU8hlmfwR_QupIvh0oqpsO44rS2PG"
