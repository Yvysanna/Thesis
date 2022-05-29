##
#
# current_listening.py
# 
# Requests what Spotify User is currently listening to
#
# SOURCECODE: https://www.youtube.com/watch?v=yKz38ThJWqE


import time
import requests
from pprint import pprint

# TODO: Automatically update after one hour
SPOTIFY_ACCESS_TOKEN = 'BQAAcfkGe8YfzFX6iftG6G_NHA8eN7vv6xHsfoxaXEQ8-C8iUxqdKktMwOCbadpv2W2S4wnZLBrM8NHnhAoEtZqo1LIZi13Qd2XmadegYMG1iJX6no-RepqMi4YkUettPHwfN4Wwn07CCZe0'
SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'


def get_current_track(access_token):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
    )

    # Read the response in json format into memory
    resp_json = response.json()

    # Pick only data we want to work with from json
    track_id = resp_json['item']['id']
    track_name = resp_json['item']['name']

    # Returns a list so we need to join artists together
    artists = resp_json['item']['artists']
    artist_name = ', '.join(
        [artist['name'] for artist in artists]
    )
    link = resp_json['item']['external_urls']['spotify']

    # Create dict with the format we want
    current_track_info = {
        'id': track_id,
        'name' : track_name,
        'artists': artist_name,
        'link': link
    }

    return current_track_info

def main():

    # Currently loops every 2 seconds to ask which song is playing
    # TODO: Make manually write or listen for event
    # TODO: Check for errors if ads or listener stops playing
    while True:
        current_track_info = get_current_track(
            SPOTIFY_ACCESS_TOKEN
        )
        
        # TODO: Write into memory
        pprint(current_track_info, indent=4)

        time.sleep(2)

if __name__ == '__main__':
    main()