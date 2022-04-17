import datetime
import requests
import pandas as pd

playlist_id = '37i9dQZF1DXcBWIGoYBM5M'

# TODO: Automatically update after one hour
SPOTIFY_ACCESS_TOKEN = 'BQDE-c_JR6OWrG4RFyOj26ElZPYsCj9j5_tT1a5OmPXbFAOWMv4jEK3q1k3VzCmDxKbAd77JI2P4zc4ZsadqYMm8ncsI2NN-158QrKUSInoBFfTHBdg0cOpllhE3zgqNwBy7QYYeK71UDUOZP_hT72enxsurpGEDdNrB4x4-'
SPOTIFY_GET_PLAYLIST = f' 	https://api.spotify.com/v1/playlists/{playlist_id}'


def get_recent_tracks(access_token: str) -> dict:
    response = requests.get(
        SPOTIFY_GET_PLAYLIST,
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
    )

    # Read the response in json format into memory
    resp_json = response.json()

    
    # Pick only data we want to work with from json
    items = resp_json['tracks']['items']

    name = resp_json['name']
    description = resp_json['description']
    image = resp_json['images'][0]['url']


    track_name = []; artists = []; duration = []; links = []; playlist = []
    for item in items:
        track_name.append(item['track']['name'])

        # Returns a list so we need to join artists together
        artists.append(';'.join([x['name'] for x in item['track']['artists']]))
        links.append(item['track']['external_urls']['spotify'])
        min, sec = divmod(divmod(item['track']['duration_ms'], 1000)[0], 60)
        duration.append(datetime.time(0, min, sec).strftime('%M:%S'))


    # Create dict with the format we want
    listening_history = {
        'name' : track_name,
        'artists': artists,
        'duration': duration,
        'link': links,
        'playlist': playlist
    }
    listening_history['playlist'] = [name]*len(track_name)

    print(len(listening_history['playlist']), len(listening_history['name']))
    return listening_history, description, image


def fill_df(listening_history: dict, name: str) -> None:

    list_df = pd.DataFrame(data=listening_history).fillna(method='bfill')  
    list_df.to_csv(f'{name}.csv', index=False, header=True)


def main():
    listening_history, description, image = get_recent_tracks(
        SPOTIFY_ACCESS_TOKEN
    )
    fill_df(listening_history, listening_history['playlist'][0])
    print(description, image, listening_history['playlist'][0])




if __name__ == '__main__':
    main()