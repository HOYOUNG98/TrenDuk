from pymongo import MongoClient, UpdateOne, InsertOne
from pandas import DataFrame

client = MongoClient("mongodb+srv://kevin4163:ghdi4163@trenduk.sucyo.mongodb.net/trenduk?retryWrites=true&w=majority")
gibo = client["beta"]["gibo_beta"]
node_collection = client["beta"]["node_beta"]


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


def upsertManyNodes(object_list):
    operations = []
    node_ids = [str(id) for id in node_collection.find().distinct("_id")]
    for node in object_list:
        if node["depth"] == 0:
            continue

        if str(node["_id"]) not in node_ids:
            operations.append(InsertOne(node))
        else:
            operations.append(
                UpdateOne({"_id": node["_id"]}, {"$push": {"data": {"$each": node["data"]}}}, upsert=True)
            )

    result = node_collection.bulk_write(operations)
    return result
