from flask import Flask, render_template, request
import json
import http.client
import urllib.parse
import os
from dotenv import load_dotenv
from matplotlib.pyplot import title

#from models
from models.user import User
from models.database import get_db
from models.watchlist import add_to_watchlist, get_watchlist
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import redirect, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey123"

# Replace these with your TMDb API keys

load_dotenv()  # loads .env file

API_LIST = os.getenv("TMDB_API_KEYS").split(",")
API_Counter = 0

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@app.route('/')
@login_required
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
# Login
# ---------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()

    if user:
        return User(user["id"], user["username"], user["password"])
    return None

@app.route("/add_to_watchlist/<int:show_id>")
@login_required
def add_to_watchlist_route(show_id):
    show_name = request.args.get("name")
    poster = request.args.get("poster")

    add_to_watchlist(current_user.id, show_id, show_name, poster)

    return redirect(url_for("show_details", show_id=show_id))

@app.route("/my_watchlist")
@login_required
def my_watchlist():
    items = get_watchlist(current_user.id)
    return render_template("watchlist.html", items=items)

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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            user_obj = User(user["id"], user["username"], user["password"])
            login_user(user_obj)

            next_page = request.args.get("next")
            return redirect(next_page or url_for("home"))

        return "Invalid username or password"

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)