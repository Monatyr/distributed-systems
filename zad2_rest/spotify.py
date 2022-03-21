from codecs import decode
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



spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

class Spotify(Resource):
    def get(self):
        try:
            files = glob.glob('templates/*.html')
            files.remove("templates\\index.html")
            for f in files:
                os.remove(f)

            args = request.args
            if args['type'] == 'artist_most_popular':
                data = get_songs(args['id'])
            elif args['type'] == 'albums':
                data = get_albums(args['id'])
            elif args['type'] == 'recommended_artists':
                data = get_recommended(args['id'])
                
            if data is None:
                return f'Sorry, we could not find the result for "{args["id"]}"'
            file_path = create_html(data)
            file_name = file_path[10:]
            file_name = file_name[:-5]
            return redirect('result/'+ file_name)
        except:
            return "An error has occured"




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
        albums = spotify.artist_albums(artist_id=artist_uri, album_type='album', limit=50)['items']
        result = []

        for album in albums:
            flag = True
            for album_in_res in result:
                if album_in_res['name'].lower() == album['name'].lower():
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
        result = []
        r = spotify.artist_top_tracks(artist_id=artist_uri, country=country)
        songs = r['tracks']

        for song in songs:
            minutes = str((song['duration_ms']//60000))
            seconds = str((song['duration_ms']//1000)%60)
            seconds = '0'+ seconds if len(seconds) == 1 else seconds
            song_len = minutes + ':' + seconds
            my_song = {'name': song['name'], 'album': song['album']['name'], 'image': song['album']['images'][0]['url'], 'time_length': song_len, 'artist': song['album']['artists'][0]['name']}
            result.append(my_song)
        
        data = {'type': 'artist_songs', 'data': result}
        return data
    except:
        print('get songs')


def get_recommended(artist_name: str):
    try:
        print(artist_name)
        print(get_arist_uri(artist_name))
        result = []
        artists = spotify.artist_related_artists(get_arist_uri(artist_name))['artists']

        for el in artists:
            name = el['name']
            followers = el['followers']['total']
            image = el['images'][0]['url']
            genres = el['genres']
            my_artist = {'name': name, 'followers': followers, 'genres': genres, 'image': image, 'artist': artist_name}
            result.append(my_artist)

        data = {'type': 'similar', 'data': result}
        return data
    except:
        pass


if __name__ == "__main__":
    get_songs('the beatles')
    get_recommended("Dire Straits")