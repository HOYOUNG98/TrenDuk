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

        d = d[2:]
        pick_rates_numerator, pick_rates_denominator = d[::4], d[1::4]
        win_rates_numerator, win_rates_denominator = d[2::4], d[3::4]

        pick_rates = [num / denom if num and denom else None for num, denom in zip(pick_rates_numerator, pick_rates_denominator)]
        win_rates = [num / denom if num and denom else None for num, denom in zip(win_rates_numerator, win_rates_denominator)]

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