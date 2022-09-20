import json
import csv
import os
import sys
import time

import pandas as pd

# We want to use same hash key to keep deterministic values across different runs
if not os.environ.get('PYTHONHASHSEED'):
    os.environ['PYTHONHASHSEED'] = '0'
    os.execv(sys.executable, ['python3'] + sys.argv)


def hello(event, context):

    target_node = event['queryStringParameters']['node']

    # Read CSV and load it as a Dataframe

    start = time.time()
    df = pd.read_csv('./data/nodes.csv.gz', compression='gzip')

    end = time.time()
    print(start-end)

    # Set the id column as index

    # Lookup the row of the target node, then load its children

    # Find stats of the children, then build response body

    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}


if __name__ == "__main__":
    hello({'queryStringParameters': {'node': 'qq'}}, {})
