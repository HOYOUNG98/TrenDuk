from io import BytesIO
import sqlite3
import boto3
from collections import defaultdict
import os


# S3
IN_BUCKET_NAME = "trenduk-serving-yearly-nodes"
OUT_BUCKET_NAME = "trenduk-speed-yearly-rates"

class WinCounter(object):
    def __init__(self):
        self.win = 0
        self.lose = 0

def precompute(event, _):
    s3_client = boto3.client('s3')
    response = s3_client.list_objects(Bucket=IN_BUCKET_NAME)

    precomputed_rows = {}

    for data in response['Contents']:
        file_name = data['Key']
        year = int(data['Key'][:4])

        if year < 2010:
            continue
        
        file = s3_client.get_object(Bucket=IN_BUCKET_NAME, Key=file_name)

        buffer = BytesIO(file['Body'].read())

        with open(file_name, 'wb') as tmp_file:
            tmp_file.write(buffer.getbuffer())

        conn = sqlite3.connect(file_name)
        cursor = conn.cursor()

        query = """
            SELECT node.node_id, node.move, node.color, node.sequence_depth, game.result
            FROM node_game
                JOIN game ON game.game_id = node_game.game_id
                JOIN node ON node.node_id = node_game.node_id;
        """

        rows = cursor.execute(query)
        win_counter = defaultdict(lambda: defaultdict(int))
        total_counter = defaultdict(int)
        for node_id, _, color, _, result in rows:
            # We have to separately count root node
            if node_id[4:] == "rootroot0root":
                total_counter["rootroot0root"] += 1

            key = "win" if result[0] == color else "lose"
            win_counter[node_id][key] += 1

            total_counter[node_id] += 1

        for node_id in total_counter.keys():
            if node_id == "rootroot0root":
                continue

            parent = node_id[4:]

            pick_rate = total_counter[node_id] / total_counter[parent]
            win_rate = win_counter[node_id]["win"] / total_counter[node_id]

            # (node_id, pick_rate, win_rate)
            if node_id not in precomputed_rows:
                precomputed_rows[node_id] = [node_id] + [None] * 26

            precomputed_rows[node_id][(year-2010)*2+1] = pick_rate
            precomputed_rows[node_id][(year-2010)*2+2] = win_rate



        os.remove(file_name)
    
    conn = sqlite3.connect(f'precomputed_v1.db')
    cursor = conn.cursor()

    substr = []
    for year in range(2010, 2023):
        substr.append(f"pick_rate_{year} INTEGER")
        substr.append(f"win_rate_{year} INTEGER")
    substr = ", ".join(substr)

    cursor.execute(f"CREATE TABLE precomputed (node_id VARCHAR(30) PRIMARY KEY, {substr});")
    
    rows = list(map(tuple,precomputed_rows.values()))
    
    substr = ["?"] * 26
    substr = ",".join(substr)

    cursor.executemany(f"INSERT INTO precomputed VALUES (?,{substr});", rows)
    conn.commit()
    cursor.close()

    if OUT_BUCKET_NAME not in s3_client.list_buckets():
        s3_client.create_bucket(Bucket=OUT_BUCKET_NAME)
        s3_client.upload_file("precomputed_v1.db", OUT_BUCKET_NAME, "precomputed_v1.db")
    
    os.remove("precomputed_v1.db")


if __name__ == "__main__":
    precompute(None,None)