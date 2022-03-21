from flask import Flask, request, redirect, url_for, render_template
from flask_restful import Api, Resource
from spotipy.oauth2 import SpotifyClientCredentials
from spotify import Spotify
import deezer

client_id = '5a9d277b38f142a0ae8a2143a854d1af'

app = Flask(__name__)
api = Api(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result/<result_name>")
def result(result_name):
    try:
        result = request.form
        return render_template(f"{result_name}.html", result=result)
    except Exception as e:
        print(e)
        return 'Could not deliver results'


def handle_bad_request(e):
    return 'Bad request!', 400

def handle_not_found(e):
    return 'Not found!', 404

def handle_internal_server(e):
    return 'Internal server error!', 500


app.register_error_handler(400, handle_bad_request)
app.register_error_handler(404, handle_not_found)
app.register_error_handler(500, handle_internal_server)

if __name__ == "__main__":
    api.add_resource(Spotify, "/search")
    app.run(debug=True)