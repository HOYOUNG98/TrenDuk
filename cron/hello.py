import time
from flask import Flask
from pymongo import MongoClient
from pandas import DataFrame, json_normalize
import os

from helper.scraper import request, parse_links, parse_game
from helper.analyzer import assort_corners, build_tree, tree_to_list

app = Flask(__name__)

os.environ["PYTHONHASHSEED"] = "TrendukSecret"

MAX_PAGE = 500


@app.cli.command()
def fetchGames():

    gibo_df = []
    for page in range(1, MAX_PAGE):
        link = "https://www.cyberoro.com/bcast/gibo.oro?param=1&div=1&Tdiv=B&Sdiv=2&pageNo={0}&blockNo=1".format(page)
        content = request(link)
        links = parse_links(content)

        for link in links:
            gibo_object = parse_game(link)

            if gibo_object == None:
                continue
            gibo_df.append(gibo_object)
        print("page {0}".format(page), len(gibo_df))
        page += 1

    gibo_df = DataFrame(gibo_df)

    # Rearrange columns so moves go to end
    cols = gibo_df.columns.tolist()
    cols = cols[0:3] + cols[4:] + [cols[3]]
    gibo_df = gibo_df[cols]

    gibo_df.to_csv("output.csv", index=False, encoding="utf-8-sig")


# @app.cli.command()
# def scheduled():
#     """Run scheduled job."""
#     for page in range(1, MAX_PAGE):
#         link = "https://www.cyberoro.com/bcast/gibo.oro?param=1&div=1&Tdiv=B&Sdiv=2&pageNo={0}&blockNo=1".format(page)
#         content = request(link)
#         links, duplicate_found = parse_links(content)

#         if duplicate_found == False and len(links) == 0:
#             print("Reached Endpoint")
#             break

#         gibo_objects = []
#         for link in links:
#             content = request(link)
#             gibo_object = parse_game(content, link)

#             if gibo_object == None:
#                 continue

#             gibo_objects.append(gibo_object)

#         page += 1

#         root = {"depth": 0, "children": []}
#         for gibo_object in gibo_objects:
#             corners = assort_corners(gibo_object["moves"])
#             for moves in corners:
#                 root = build_tree(root, moves, gibo_object)

#         node_list = tree_to_list(root)

#         insertManyGibos(gibo_objects)
#         upsertManyNodes(node_list)

#         if duplicate_found == False:
#             print("Duplicate Found: Ending Process")
#             break


# @app.cli.command()
# def test1():
#     link = "https://www.cyberoro.com/bcast/gibo.oro?param=1&div=1&Tdiv=B&Sdiv=2&pageNo=1&blockNo=1"
#     content = request(link)
#     links, _ = parse_links(content)

#     gibo_documents = []

#     for link in links[:2]:
#         content = request(link)
#         gibo_document = parse_game(content, link)

#         gibo_documents.append(gibo_document)

#     root = {"depth": 0, "children": []}
#     for gibo_document in gibo_documents:
#         corners = assort_corners(gibo_document["moves"])
#         for moves in corners:
#             root = build_tree(root, moves, gibo_document)

#     node_list = tree_to_list(root)

#     df = DataFrame(node_list)
#     df["len"] = df["data"].str.len()
#     print(df.sort_values(by=["len"], ascending=False))

#     insertManyGibos(gibo_documents)
#     upsertManyNodes(node_list)
#     result = upsertManyNodes(node_list)
#     print(result)


@app.cli.command()
def test2():
    df = fetchAllGibos()
    print(df.head())


@app.route("/")
def hello_world():
    return "Hello, World!"
