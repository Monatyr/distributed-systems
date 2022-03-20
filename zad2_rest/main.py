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

@app.route("/result/<result_name>", methods=['GET', 'POST'])
def result(result_name):
    print("RESULT: ",result_name)
    result = request.form
    return render_template(f"{result_name}.html", result=result)



if __name__ == "__main__":
    api.add_resource(Spotify, "/search")
    app.run(debug=True)