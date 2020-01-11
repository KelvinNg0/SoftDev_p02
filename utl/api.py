import urllib.request
import json

baseurl = "https://www.speedrun.com/api/v1/leaderboards/2689591p/category/rklr48kn?embed=players"

#Returns an array of dictionaries containing the necessary data per run
def get_leaderboards():
    url = urllib.request.urlopen(baseurl)
    response = url.read()
    data = json.loads(response)['data']
    runs_json = data['runs']
    players_json = data['players']['data']

    runs = [] # arr of dicts

    for i in range(0, len(runs_json)):
        dict = {}
        dict['place'] = runs_json[i]['place'] #1st, 2nd, 3rd, etc.
        dict['time'] = runs_json[i]['run']['times']['realtime_t'] #in seconds
        dict['player'] = players_json[i]['names']['international']
        runs.append(dict)

    return runs
