from steamcheck import app
from flask import jsonify
import os
import steamapi
import json


@app.route('/')
def index():
    return "Hello I am working YAY!"


@app.route('/report/<name>')
def report(name=None):
    """
    This will generate the report based on the users Steam ID.  Returns JSON
    :param name: Steam ID (either numerical ID or vanity url: steamcommunity.com/id/moird
    :return: Json object that contains listing of all linux games and general information about them:
    {
        "steamuser": "real steam name",
        "image": "steam user image url",
        "games": [{'gametitle', {"linux":true}}]
        "error": ""
    }
    """
    process_report = {}
    try:
        with open('./SteamLinux/GAMES.json') as linux_game_list_raw:
            linux_games = json.load(linux_game_list_raw)

        with open('./winehq.json') as winehq_raw:
            winehq_apps = json.load(winehq_raw)

        steam_connection = steamapi.core.APIConnection(api_key=os.environ['steam_api_key'])

        try:
            user = steamapi.user.SteamUser(userid=int(name))
        except ValueError:
            # When we get further this as a fallback will be taken out, really don't want to do this.
            user = steamapi.user.SteamUser(userurl=name)

        process_report['steamuser'] = user.name
        process_report['image'] = user.avatar
        process_report['games'] = {}
        for game in user.games:
            linux = False
            winehq = False
            if str(game.id) in linux_games:
                linux = True
            if game.name in winehq_apps:
                winehq = winehq_apps[game.name]
            process_report['games'][game.id] = {"name": game.name, "linux": linux, "winehq":winehq}
    except Exception as e:
        process_report['error'] = e
    return jsonify(**process_report)