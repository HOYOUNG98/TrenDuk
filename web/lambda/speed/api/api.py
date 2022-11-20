import sqlite3
import json


def rates_by_parent(event, _):

    parent = event['queryStringParameters']['parent']

    # query from database
    conn = sqlite3.connect(f'precomputed_v1.db')
    cursor = conn.cursor()

    query = f"SELECT * FROM precomputed WHERE parent_id='{parent}';"
    res = cursor.execute(query)
    
    data = {}
    for d in res.fetchall():
        key = d[0]
        data[key] = {"pick_rates": [], "win_rates": []}

        pick_rates = d[1:-1][::2]
        win_rates = d[1:-1][1::2]
        for i in range(13):
            data[key]['pick_rates'].append({"year":2010+i, "rate":pick_rates[i]})
            data[key]['win_rates'].append({"year":2010+i, "rate":win_rates[i]})


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
    res = rates_by_parent({"queryStringParameters": {"parent": "rootroot0root"} }, {})
    print(res)