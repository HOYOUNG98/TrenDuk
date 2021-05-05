import time
from flask import Flask
from pymongo import MongoClient
from pandas import DataFrame

from helper.scraper import request, parse_links, parse_game
from helper.analyzer import assort_corners, build_tree, tree_to_list
from helper.database import fetchAllGibos, insertManyGibos, insertManyNodes

app = Flask(__name__)


MAX_PAGE = 465


@app.cli.command()
def scheduled():
    """Run scheduled job."""
    for page in range(1, MAX_PAGE):
        link = "https://www.cyberoro.com/bcast/gibo.oro?param=1&div=1&Tdiv=B&Sdiv=2&pageNo={0}&blockNo=1".format(page)
        content = request(link)
        links, duplicate_found = parse_links(content)

        if duplicate_found == False:
            print("DUPLICATE")
            break

        gibo_objects = []
        for link in links:
            content = request(link)
            gibo_object = parse_game(content, link)

            if gibo_object == None:
                continue

            gibo_objects.append(gibo_object)
        print(DataFrame(gibo_objects).head())
        insertManyGibos(gibo_objects)

        page += 1

        print("Estimated: {0}/{1}".format(page, MAX_PAGE))

        root = {"depth": 0, "children": []}
        for gibo_object in gibo_objects:
            corners = assort_corners(gibo_object["moves"])
            for moves in corners:
                root = build_tree(root, moves, gibo_object)

        node_list = tree_to_list(root, assignedID=hash("root_hash"))

        insertManyNodes(node_list)


@app.cli.command()
def test1():
    link = "https://www.cyberoro.com/bcast/gibo.oro?param=1&div=1&Tdiv=B&Sdiv=2&pageNo=1&blockNo=1"
    content = request(link)
    links, _ = parse_links(content)

    gibo_documents = []

    for i in range(5):
        content = request(links[i])
        gibo_document = parse_game(content, links[i])

        gibo_documents.append(gibo_document)

    root = {"depth": 0, "children": []}
    for gibo_document in gibo_documents:
        corners = assort_corners(gibo_document["moves"])
        for moves in corners:
            root = build_tree(root, moves, gibo_document)

    node_list = tree_to_list(root)

    df = DataFrame(node_list)
    df["len"] = df["data"].str.len()
    print(df.sort_values(by=["len"], ascending=False))


@app.cli.command()
def test2():
    df = fetchAllGibos()
    print(df.head())


@app.route("/")
def hello_world():
    return "Hello, World!"
