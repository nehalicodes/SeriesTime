from flask import Flask, render_template, request
import json
import http.client
import urllib.parse
import os
from dotenv import load_dotenv
from matplotlib.pyplot import title


app = Flask(__name__)

# Replace these with your TMDb API keys

load_dotenv()  # loads .env file

API_LIST = os.getenv("TMDB_API_KEYS").split(",")
API_Counter = 0


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/seriesGraph', methods=['POST', 'GET'])
def seriesGraph():
    title = request.args.get('seriesTitle')
    seriesKey = getSeriesKey(title)
    seasons = getSeriesSeasons(seriesKey)
    seriesName, labelsList, valuesList, episodeTitlesList = getTMDBData(seriesKey, seasons)

    return render_template(
        "darkGraphWithCSS.html",
        seriesName=seriesName,
        labelsList=labelsList,
        valuesList=valuesList,
        episodeTitlesList=episodeTitlesList,
        seasonCount=len(labelsList)
    )


# ---------------------------------------------------------
# 1. SEARCH SERIES (TMDb)
# ---------------------------------------------------------
def getSeriesKey(title):
    conn = http.client.HTTPSConnection("api.themoviedb.org", 443)

    encoded = urllib.parse.quote(title)
    endpoint = f"/3/search/tv?api_key={API_LIST[API_Counter]}&query={encoded}"

    conn.request("GET", endpoint)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))

    return data['results'][0]['id']


# ---------------------------------------------------------
# 2. GET SEASONS (TMDb)
# ---------------------------------------------------------
def getSeriesSeasons(seriesKey):
    conn = http.client.HTTPSConnection("api.themoviedb.org", 443)

    endpoint = f"/3/tv/{seriesKey}?api_key={API_LIST[API_Counter]}"
    conn.request("GET", endpoint)

    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))

    # Skip season 0 (specials)
    seasons = [str(s['season_number']) for s in data['seasons'] if s['season_number'] != 0]
    return seasons


# ---------------------------------------------------------
# 3. GET EPISODE RATINGS (TMDb)
# ---------------------------------------------------------
def getTMDBData(seriesKey, seasons):
    labelsList = []
    valuesList = []
    episodeTitlesList = []
    seriesName = ""

    for season in seasons:
        conn = http.client.HTTPSConnection("api.themoviedb.org", 443)
        endpoint = f"/3/tv/{seriesKey}/season/{season}?api_key={API_LIST[API_Counter]}"
        conn.request("GET", endpoint)

        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))

        seriesName = data['name']

        l = []
        v = []
        t = []

        for ep in data['episodes']:
            l.append(str(ep['episode_number']))
            v.append(float(ep['vote_average']))
            t.append(f"S{season}E{ep['episode_number']}: {ep['name']}")

        labelsList.append(l)
        valuesList.append(v)
        episodeTitlesList.append(t)

    return seriesName, labelsList, valuesList, episodeTitlesList


if __name__ == "__main__":
    app.run(debug=True)