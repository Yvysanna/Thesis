##
#
# current_listening.py
# 
# Requests what Spotify User was previously listening
# Absolute limit is 50 previously listened tracks
#
# Inspired by get current listening from https://www.youtube.com/watch?v=yKz38ThJWqE

import requests
import pandas as pd

# TODO: Automatically update after one hour
LIMIT = 50
SPOTIFY_ACCESS_TOKEN = 'BQALb8v8yFu3caqvAOQLAfeef4b47pDJT6Yw6NvAGLUoeubaziO5ZNOlJW59gKhelx7jg_522MA7GAt2Fa1ToKXq-yKWTBh_D8Mx81frIh_m92pvMmAU2cyj4NHbCvubBbaNlXYNqyK9HXt3oZ-fNXPy00bEplTqOdnbSZHp'
SPOTIFY_GET_RECENT = f'https://api.spotify.com/v1/me/player/recently-played?limit={LIMIT}'


def get_recent_tracks(access_token: str) -> dict:
    response = requests.get(
        SPOTIFY_GET_RECENT,
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
    )

    # Read the response in json format into memory
    resp_json = response.json()

    
    # Pick only data we want to work with from json
    items = resp_json['items']

    t = []; track_id = []; track_name = []; artists = []; links = []; playlist = []
    for item in items:
        t.append(item['played_at'][:-5])
        playlist.append(item['context']['external_urls']['spotify'])
        track_id.append(item['track']['id'])
        track_name.append(item['track']['name'])

        # Returns a list so we need to join artists together
        artists.append(';'.join([x['name'] for x in item['track']['artists']]))
        links.append(item['track']['external_urls']['spotify'])


    # Create dict with the format we want
    listening_history = {
        'time': t,
        'id': track_id,
        'name' : track_name,
        'artists': artists,
        'link': links,
        'playlist': playlist
    }
    return listening_history


def fill_df(listening_history: dict) -> None:

    # Read old DF and create new DF
    old = pd.read_csv('listening_history.csv')
    hist_df = pd.DataFrame(data=listening_history)    

    # Concat and write into memory
    df_diff = pd.concat([old, hist_df],ignore_index=True).drop_duplicates()
    df_diff.to_csv('listening_history.csv', index=False, header=True)


def main():
    current_history = get_recent_tracks(
        SPOTIFY_ACCESS_TOKEN
    )
    fill_df(current_history)




if __name__ == '__main__':
    main()
