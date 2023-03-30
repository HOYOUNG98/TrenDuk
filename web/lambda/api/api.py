import sqlite3
import json


def rates_by_parent(event, _):

    parent = event['queryStringParameters']['parent']

    # query from realtime view database
    realtime_conn = sqlite3.connect('realtime_view.db')
    realtime_cursor = realtime_conn.cursor()

    realtime_query = f"SELECT * FROM precomputed WHERE parent_id='{parent}';"
    res = realtime_cursor.execute(realtime_query)

    realtime_data = {}
    for d in res.fetchall():
        key = d[0]
        if all(d[-4:]):
            realtime_data[key] = {"win": d[-4] / d[-3], "pick": d[-2] / d[-1]}

    # query from batch view database
    conn = sqlite3.connect('batch_view.db')
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
        
        if key in realtime_data:
            data[key]['pick_rates'][-1]['rate'] = realtime_data[key]['pick']
            data[key]['win_rates'][-1]['rate'] = realtime_data[key]['win']


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