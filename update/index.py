# library imports
from flask import Flask
from pandas import read_csv, DataFrame
import csv

# local imports
from crawler import parseGame, parsePage
from analyzer import assortCorners

app = Flask(__name__)


@app.cli.command()
def updateGames():
    '''catch up games from cyberoro'''

    original_df = read_csv('cyberoro_games.csv')
    latest_link = original_df.iloc[0]["link"]
    gibo_list = []
    for page in range(1, 800):
        link = "https://www.cyberoro.com/bcast/gibo.oro?param=1&div=1&Tdiv=B&Sdiv=2&pageNo={0}&blockNo=1".format(
            page)
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

    gibo_df.to_csv("cyberoro_games.csv", index=False,
                   encoding="utf-8-sig", quotechar='"', quoting=csv.QUOTE_ALL)

    for gibo in gibo_list:
        moves = gibo["move"].split(";")
        print(assortCorners(moves))
