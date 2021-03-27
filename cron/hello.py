import time
from flask import Flask
from pymongo import MongoClient

from helper.scraper import request, parse_links, parse_game

app = Flask(__name__)
client = MongoClient(
    "mongodb+srv://kevin4163:ghdi4163@trenduk.sucyo.mongodb.net/trenduk?retryWrites=true&w=majority")
gibo = client['trenduk']['gibo_beta']


@app.cli.command()
def scheduled():
    """Run scheduled job."""
    duplicate_found = True
    page = 1
    count = 0
    while duplicate_found:
        link = "https://www.cyberoro.com/bcast/gibo.oro?param=1&div=1&Tdiv=B&Sdiv=2&pageNo={0}&blockNo=1".format(
            page)
        content = request(link)
        links, duplicate_found = parse_links(content)
        for link in links:
            content = request(link)
            parse_game(content)
            count += 1
        page += 1
        print(page)
    print(count)


@app.route('/')
def hello_world():
    print(gibo.find({"link"}))
    return 'Hello, World!'
