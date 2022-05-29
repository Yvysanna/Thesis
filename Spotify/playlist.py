import datetime
import requests
import pandas as pd

# Today's Top Hits
#playlist_id = '37i9dQZF1DXcBWIGoYBM5M'


# Mixtape 1
#playlist_id = '37i9dQZF1E38KwlR1zxCgm'
#playlist_id = '37i9dQZF1E36P2l4sUXzYX'

# Mixtape 2
#playlist_id = '37i9dQZF1E37ohPS9wcQMn'
#playlist_id = '37i9dQZF1E34ZFZDD1YOfI'

# Mixtape 3
#playlist_id = '37i9dQZF1E35UGygQXxfCr'
#playlist_id = '37i9dQZF1E36nktpVoXB14'

# Mixtape 4
#playlist_id = '37i9dQZF1E37zOtUByg3ii'
#playlist_id = '37i9dQZF1E38N0MsE8ZLqn'

# Mixtape 5
# playlist_id = '37i9dQZF1E3556dnEO8irM'
#playlist_id = '37i9dQZF1E37xbiyjDLqwJ'

# Mixtape 6
# playlist_id = '37i9dQZF1E38QLDAj1w9oD'
#playlist_id = '37i9dQZF1E38tI6Ipxh8ww'

# TODO: Automatically update after one hour
#SPOTIFY_ACCESS_TOKEN = 'BQCh7C7mvUvehJI6kJGNnorGM3YwIOFu_iOJ2iOBEkCb-CCkRrdkHXqL0Kjlkut7_8Qb0EtCA7J88pn2sg215dCTZ0UvORMbTj6agSMXqdAGy__ShPxqKVoFkJnTa8ymXAQSuhSryLUraUB8wk68edURqQMXEmoY0yOligR5pEbWYwa8jT6saAgGhg'
SPOTIFY_ACCESS_TOKEN ='BQCKnK266Gx4U4yvXFbIAdiizJD7vIvIKRMS_2I3SpHixL8n412DVkafQTFZ4fIivaBzuOSOkFgS8xhOaaQ6gi3lCNrtIvi0TNVyTkSNJW_qxF5OK76uP_ID24GT23TBgptfGEQEd9GfoIHMKRWanFlzzWcWP_GumaYlPeCBOLKtpu1AOuJJAeYXqCqsIQ'
#SPOTIFY_GET_PLAYLIST = f'https://api.spotify.com/v1/playlists/{playlist_id}'


def get_recent_tracks(access_token: str, SPOTIFY_GET_PLAYLIST) -> dict:
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
        'playlist': [name]*len(track_name),
        'name' : track_name,
        'artists': artists,
        'duration': duration,
        'link': links,
    }
    

    with open('data/playlist.txt', 'a') as f:
        f.write(f'name: {listening_history["playlist"][0]}\ndescription: {description}\nimg ref: {image}\nid: {playlist_id}\n\n')
    print(len(listening_history['playlist']), len(listening_history['name']))
    return listening_history, description, image


def fill_df(listening_history: dict, name: str) -> None:

    list_df = pd.DataFrame(data=listening_history).fillna(method='bfill')  
    list_df.to_csv(f'data/Female {name} End.csv', index=False, header=True)


def main(pl):
    listening_history, description, image = get_recent_tracks(
        SPOTIFY_ACCESS_TOKEN, pl
    )
    fill_df(listening_history, listening_history['playlist'][0])
    print(description, image, listening_history['playlist'][0])




if __name__ == '__main__':
    playlist_id = ['37i9dQZF1E36P2l4sUXzYX','37i9dQZF1E34ZFZDD1YOfI','37i9dQZF1E36nktpVoXB14','37i9dQZF1E38N0MsE8ZLqn','37i9dQZF1E37xbiyjDLqwJ','37i9dQZF1E38tI6Ipxh8ww']
# ['37i9dQZF1E38KwlR1zxCgm',
#     '37i9dQZF1E37ohPS9wcQMn',
#     '37i9dQZF1E35UGygQXxfCr',
#     '37i9dQZF1E37zOtUByg3ii',
#     '37i9dQZF1E3556dnEO8irM',
#     '37i9dQZF1E38QLDAj1w9oD'
#     ]
    SPOTIFY_GET_PLAYLIST = f'https://api.spotify.com/v1/playlists/{playlist_id}' 
    for id in playlist_id:
        main(f'https://api.spotify.com/v1/playlists/{id}')