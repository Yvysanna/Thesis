
import base64
from datetime import datetime, timedelta
from urllib.parse import urlencode
import pandas as pd
import requests


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.now()
    access_token_did_expire = True

    client_id = None
    client_secret = None
    token_url = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id, client_secret, *args, **kwargs) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self) -> str:
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id == None or client_secret == None:
            raise Exception("check Client IDs")
        client_creds = f'{client_id}:{client_secret}'
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_header(self) -> dict:
        client_creds_b64 = self.get_client_credentials()
        return {"Authorization": f"Basic {client_creds_b64}"}

    def get_token_data(self) -> dict:
        return {"grant_type": "client_credentials"} 

    def perform_auth(self) -> bool:
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_header()
 
        r = requests.post(token_url, data = token_data, headers = token_headers)
        if r.status_code not in range(200, 299):
            print("Could not authenticate client")
        data = r.json()
        now = datetime.now()
        access_token = data["access_token"]
        expires_in = data["expires_in"]
        expires = now + timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self) -> str:
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.now()

        if token == None or expires < now:
            self.perform_auth()
            return self.get_access_token()
        return token


    def search(self, query, search_type="artist") -> dict: 
        access_token = self.get_access_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        data = {"q": query, "type": search_type.lower()}
        search_url = f"https://api.spotify.com/v1/search?{urlencode(data)}"
        search_r = requests.get(search_url, headers=headers)
        if search_r.status_code not in range(200, 299):
            print("Encountered search issue")
        json_search = search_r.json()
        # print(json_search)
        return json_search

    def get_tracks(self, query, search_type="track") -> list:
        resp = self.search(query, search_type)
        all = []
        for i in range(len(resp['tracks']['items'])):
            track_name = resp['tracks']['items'][i]['name']
            track_id = resp['tracks']['items'][i]['id']
            artist_name = resp['tracks']['items'][i]['artists'][0]['name']
            artist_id = resp['tracks']['items'][i]['artists'][0]['id']
            album_name = resp['tracks']['items'][i]['album']['name']
            images = resp['tracks']['items'][i]['album']['images'][0]['url']

            raw = [track_name, track_id, artist_name, artist_id, album_name, images]
            all.append(raw)
        return all

    def get_recommendations(self, limit=5, seed_artists='', seed_tracks='', seed_genres='rock', market='DE') -> list:
        access_token = self.get_access_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        query = f"limit={limit}&seed_artists={seed_artists}&seed_tracks={seed_tracks}&seed_genres={seed_genres}&market={market}"
        endpoint_url = f"https://api.spotify.com/v1/recommendations?{query}"
        response = requests.get(endpoint_url, headers=headers)
        if response.status_code not in range(200, 299):
            print("Encountered recommendations issue")
        json_response = response.json()
        # print('Recommended songs')
        all_reccs = []
        for i, j in enumerate(json_response["tracks"]):
            track_name = j['name']
            artist_name = j['artists'][0]['name']
            link = j['artists'][0]['external_urls']['spotify']
            # print(f"{i+1}) \"{track_name}\" by {artist_name}")
            reccs = [track_name, artist_name, link]
            all_reccs.append(reccs)
        return all_reccs


    

if __name__ == "__main__":

    CLIENT_ID='b5cc18eed4c94384b37775994f4dde36'
    CLIENT_SECRET='36e0ed19b9a948818b1935736e29ed8e'
    client = SpotifyAPI(CLIENT_ID, CLIENT_SECRET)
    search = "Hello"
    all = client.get_tracks(search, search_type="track")
    df = pd.DataFrame(all, columns=['track_name', 'track_id', 'artist_name', 'artist_id', 'album_name', 'images'])
    print('Searched songs')
    print(df)
    artistid = df['artist_id'].iloc[0]
    trackid = df['track_id'].iloc[0]
    limit = 20
    reccs = client.get_recommendations(limit=limit, seed_artists=str(artistid), seed_tracks=str(trackid))
    df2 = pd.DataFrame(reccs, columns=["Songs", "Artists", "Link"]).rename_axis('Index', axis=1)
    print('Recommended songs')
    print(df2)
