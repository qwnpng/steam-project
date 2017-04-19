from flask import Flask, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import os
import requests

app = Flask(__name__)
steam_key = os.environ['STEAM_API_KEY']


@app.route('/')
def index():
    """ Homepage """

    return render_template('index.html')


@app.route('/get_user', methods=['GET'])
def get_user():
    """ Get steam user info """

    nickname = request.args.get('nickname')

    r_id = requests.get('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={}&vanityurl={}'.format(steam_key, nickname))
    steamid = r_id.json()['response']['steamid']

    r_user = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}'.format(steam_key, steamid))
    profile_url = r_user.json()['response']['players'][0]['profileurl']

    r_games = requests.get('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}'.format(steam_key, steamid))
    game_count = r_games.json()['response']['game_count']
    games = r_games.json()['response']['games']

    return jsonify({'steamid': steamid,
                    'profileurl': profile_url,
                    'gamecount': game_count,
                    'games': games})

if __name__ == "__main__":
    app.debug = False
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
