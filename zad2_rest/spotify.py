from flask import Flask, request, redirect
from flask_restful import Api, Resource
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import base64
import json
from html_result import create_html
import os
import glob

SPOTIPY_CLIENT_ID = '5a9d277b38f142a0ae8a2143a854d1af'
SPOTIPY_CLIENT_SECRET =  '42c0c2c983914182a79764af09a60618'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))


class Spotify(Resource):
    # def __init__(self, api):
    #     print("hel")
    #     self.api = api

    def get(self):
        files = glob.glob('templates/*.html')
        files.remove("templates\\index.html")
        for f in files:
            os.remove(f)
        # print("FILES: ", files)
        args = request.args

        if args['type'] == 'artist_most_popular':
            data = get_songs(args['id'])
            file_path = create_html(data)
        elif args['type'] == 'albums':
            data = get_albums(args['id'])
            file_path = create_html(data)
        else:
            print("TO IMPLEMENT")

        file_name = file_path[10:]
        file_name = file_name[:-5]
        return redirect('result/'+ file_name)




def get_token():
    #credentials for token
    payload = {
        'grant_type': 'client_credentials',
        'client_id': SPOTIPY_CLIENT_ID,
        'client_secret': SPOTIPY_CLIENT_SECRET,
    }

    credentials_bytes = (SPOTIPY_CLIENT_ID + ':' + SPOTIPY_CLIENT_SECRET).encode("ascii")
    base64_cred_bytes = base64.b64encode(credentials_bytes)
    base64_credentials = base64_cred_bytes.decode("ascii")
    headers = {'Authorization': 'Basic ' + base64_credentials}

    #authorization token
    r = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=payload)
    r_json = r.content.decode('utf-8').replace("'", '"')
    data = json.loads(r_json)
    access_token = data['access_token']
    authorization = {'Authorization': f'Bearer {access_token}'}
    return authorization


def get_arist_uri(artist_name: str):
    try:
        authorization = get_token()
        r = requests.get(f'https://api.spotify.com/v1/search?q={artist_name.capitalize()}&type=artist&limit=1', headers=authorization)
        r_json = r.content.decode('utf-8').replace("'", '"')
        data = json.loads(r_json)
        artist_uri = data['artists']['items'][0]['id']
        return artist_uri
    except:
        print(f'ERROR: No artist named "{artist_name}"')


def get_albums(artist_name: str):
    try:
        artist_uri = get_arist_uri(artist_name)
        albums = spotify.artist_albums(artist_id=artist_uri, album_type='album', limit=10)['items']
        result = []

        for album in albums:
            flag = True
            for album_in_res in result:
                if album_in_res['name'] == album['name']:
                    flag = False
                    break
            if flag:
                my_album = {'name': album['name'], 'release_date': album['release_date'], 'artist': album['artists'][0]['name'],\
                            'tracks': album['total_tracks'], 'image': album['images'][0]['url']}
                result.append(my_album)

        data = {'type': 'albums', 'data': result}
        return data
    except:
        print("WRONG NAME")


def get_songs(artist_name: str, country: str = 'US'):
    try:
        artist_uri = get_arist_uri(artist_name)
        albums = spotify.artist_albums(artist_id=artist_uri, album_type='album', limit=10)['items']
        result = spotify.artist_top_tracks(artist_id=artist_uri, country=country)
        songs = result['tracks']
        for song in songs:
            print(song['name'], song['album']['name'], print(song['album']['images'][0]['url']))
    except:
        print('get songs')


if __name__ == "__main__":

    get_albums('The Beatles')
    # get_songs('the beatles')