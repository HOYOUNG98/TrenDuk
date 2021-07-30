# library imports
from flask import Flask, request
from flask_cors import CORS
from pandas import read_csv, DataFrame
from os import listdir
import csv

# local imports
from crawler import parseGame, parsePage
from analyzer import assortCorners

app = Flask(__name__)
CORS(app)

# Initialize database...?
games_df = read_csv("cyberoro_games.csv")
nodes_df = read_csv("cyberoro_nodes.csv")


@app.route("/")
def index():
    return "Hello World"


@app.route("/getGibo")
def getGibo():
    link = request.args.get("link", type=str)
    game = games_df.loc[games_df["link"] == link]

    return {"status": 200, "game": game.to_dict("records")}


@app.route("/getGibosByMove")
def getGibosBymove():
    move = request.args.get("move", default=0, type=str)
    parent = request.args.get("parent", default="root", type=str)
    color = request.args.get("color", default="B", type=str)

    move = nodes_df.loc[(nodes_df["move"] == move) & (nodes_df["parent"] == parent) & (nodes_df["color"] == color)]
    gibos = move.iloc[0]["link"]

    return {"status": 200, "gibos": gibos}


@app.route("/getBranches")
def getBranches():
    filenames = listdir("./data/moves")
    depth = request.args.get("depth", default=0, type=int)
    parent = request.args.get("parent", default="root", type=str)
    color = request.args.get("color", default="B", type=str)

    branches = []
    filenames.sort()
    for file in filenames:
        nodes_df = read_csv("./data/moves/" + file)

        popular_moves = nodes_df.loc[
            (nodes_df["depth"] == depth) & (nodes_df["parent"] == parent) & (nodes_df["color"] == color)
        ].sort_values(by=["num_data"], ascending=False)[:5]
        popular_moves["num_total"] = popular_moves["num_data"].sum()

        # get win percentage
        popular_moves["win_percentage"] = round(popular_moves["num_win"] / popular_moves["num_data"] * 100, 1)

        # get pick percentage
        popular_moves["pick_percentage"] = round(popular_moves["num_data"] / popular_moves["num_total"] * 100, 1)

        popular_moves = popular_moves.drop(columns=["link", "num_data", "num_win", "num_total", "parent"])
        popular_moves["year"] = file[:4]

        branches.append(popular_moves.to_dict("records"))

    if len([inner for outer in branches for inner in outer]) == 0:
        return {"status": 200, "message": "no moves meets given criteria"}

    return {"status": 200, "branches": branches}


@app.cli.command()
def updateGames():
    """catch up games from cyberoro"""

    original_df = read_csv("cyberoro_games.csv")
    latest_link = original_df.iloc[0]["link"]
    gibo_list = []
    for page in range(1, 800):
        link = "https://www.cyberoro.com/bcast/gibo.oro?param=1&div=1&Tdiv=B&Sdiv=2&pageNo={0}&blockNo=1".format(page)
        links = parsePage(link, latest_link)
        print(len(links))

        for link in links:
            gibo = parseGame(link)
            if gibo:
                gibo_list.append(gibo)
            else:
                continue

        # Prevent duplicates
        if len(links) != 20:
            break

    gibo_df = DataFrame(gibo_list)

    # fetch original csv to preprend DF
    gibo_df = gibo_df.append(original_df, sort=False)

    gibo_df.to_csv("cyberoro_games.csv", index=False, encoding="utf-8-sig", quotechar='"', quoting=csv.QUOTE_ALL)

    for gibo in gibo_list:
        moves = gibo["move"].split(";")
        print(assortCorners(moves))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
