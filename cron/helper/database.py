from pymongo import MongoClient, UpdateOne
from pandas import DataFrame

client = MongoClient("mongodb+srv://kevin4163:ghdi4163@trenduk.sucyo.mongodb.net/trenduk?retryWrites=true&w=majority")
gibo = client["beta"]["gibo_beta"]
node = client["beta"]["node_beta"]


def insertManyGibos(object_list):
    gibo.insert_many(object_list)


def insertManyNodes(object_list):
    node.insert_many(object_list)


def fetchAllGibos():
    df = DataFrame(list(gibo.find()))
    return df


def fetchAllNodes():
    df = DataFrame(list(node.find()))
    return df


def updateManyNodes(object_list):
    operations = []
    for node in object_list:
        operations.append(UpdateOne({"_id": node["_id"]}, {}))
