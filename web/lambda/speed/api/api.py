import sqlite3
import json


def rates_by_child(event, _):

    child = event['queryStringParameters']['child']

    # query from database
    conn = sqlite3.connect(f'precomputed_v1.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    query = f"SELECT * FROM precomputed WHERE node_id='{child}';"
    res = cursor.execute(query)
    data = res.fetchone()

    return {
        "isBase64Encoded": True,
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(data)
    }

def dict_factory(cursor, row):
    table = {}
    for idx, col in enumerate(cursor.description):
        table[col[0]] = row[idx]
    return table

if __name__ == "__main__":
    res = rates_by_child({"queryStringParameters": {"child": "pqB1rootroot0root"} }, {})
    print(res)