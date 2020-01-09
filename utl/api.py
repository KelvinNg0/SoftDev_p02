import urllib.request
import json

baseurl = "https://www.speedrun.com/api/v1/leaderboards/2689591p/category/rklr48kn?embed=players"

class Run {
    def __init__(self, place, time):
        self.place = place
        self.time = time
}

def get_leaderboards():
    url = urllib.request.urlopen(baseurl)
    response = url.read()
    runs_json_list = json.loads(response)['data']['runs']
    #print(runs_json_list[0])
    runs_list = []

    for element in runs_json_list:
        runs_list.append(Run(element['place'], element['run']['realtime_t']))

get_leaderboards()
