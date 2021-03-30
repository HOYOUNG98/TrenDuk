import time
from flask import Flask
from pymongo import MongoClient

from helper.scraper import request, parse_links, parse_game
from helper.analyzer import assort_corners, build_tree, tree_to_list

app = Flask(__name__)
client = MongoClient("mongodb+srv://kevin4163:ghdi4163@trenduk.sucyo.mongodb.net/trenduk?retryWrites=true&w=majority")
gibo = client["beta"]["gibo_beta"]
node = client["beta"]["node_beta"]

MAX_PAGE = 465


@app.cli.command()
def scheduled():
    """Run scheduled job."""
    for page in range(1, MAX_PAGE):
        link = "https://www.cyberoro.com/bcast/gibo.oro?param=1&div=1&Tdiv=B&Sdiv=2&pageNo={0}&blockNo=1".format(page)
        content = request(link)
        links, duplicate_found = parse_links(content)

        if duplicate_found == False:
            break

        gibo_documents = []
        for link in links:
            content = request(link)
            gibo_document = parse_game(content, link)

            if gibo_document == None:
                continue

            gibo_documents.append(gibo_document)
        gibo.insert_many(gibo_documents)

        page += 1

        print("Estimated: {0}/{1}".format(page, MAX_PAGE))

        root = {"Root": True, "Children": []}
        for gibo_document in gibo_documents:
            corners = assort_corners(gibo_document["Moves"])
            for moves in corners:
                root = build_tree(root, moves, gibo_document)

        node_list = tree_to_list(root, assignedID=hash("root_hash"))

        node.insert_many(node_list)


@app.cli.command()
def test1():
    link = "https://www.cyberoro.com/bcast/gibo.oro?param=1&div=1&Tdiv=B&Sdiv=2&pageNo=1&blockNo=1"
    content = request(link)
    links, duplicate_found = parse_links(content)

    gibo_documents = []
    link = links[0]
    content = request(link)
    gibo_document = parse_game(content, link)

    gibo_documents.append(gibo_document)
    gibo.insert_many(gibo_documents)

    root = {"Root": True, "Children": []}
    for gibo_document in gibo_documents:
        corners = assort_corners(gibo_document["Moves"])
        for moves in corners:
            root = build_tree(root, moves, gibo_document)

    node_list = tree_to_list(root, assignedID=hash("root_hash"))

    node.insert_many(node_list)


@app.route("/")
def hello_world():
    print(gibo.find({"link"}))
    return "Hello, World!"
