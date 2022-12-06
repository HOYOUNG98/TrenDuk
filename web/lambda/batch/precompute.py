import sqlite3
import boto3
import os

from collections import defaultdict
from datetime import date
from tqdm import tqdm

# S3
OUT_BUCKET_NAME = "trenduk-serving"

def precompute():

    precomputed_rows = {}

    for source_file in tqdm(os.listdir("tmp/sql_shards")):
        year = int(source_file.split(".")[0])

        if year < 2010:
            continue
        
        conn = sqlite3.connect("tmp/sql_shards/" + source_file)
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

            if node_id not in precomputed_rows:
                precomputed_rows[node_id] = [node_id, parent] + [None] * 52 

            precomputed_rows[node_id][(year-2010)*4+2] = total_counter[node_id]
            precomputed_rows[node_id][(year-2010)*4+3] = total_counter[parent]
            precomputed_rows[node_id][(year-2010)*4+4] = win_counter[node_id]['win']
            precomputed_rows[node_id][(year-2010)*4+5] = total_counter[node_id]

    # if initial:
    conn = sqlite3.connect(f"tmp/{date.today()}.db")
    cursor = conn.cursor()

    substr = []
    for year in range(2010, 2023):
        substr.append(f"pick_rate_numerator{year} INTEGER")
        substr.append(f"pick_rate_denominator{year} INTEGER")
        substr.append(f"win_rate_numerator{year} INTEGER")
        substr.append(f"win_rate_denominator{year} INTEGER")
    substr = ", ".join(substr)

    cursor.execute(f"CREATE TABLE precomputed (node_id VARCHAR(30) PRIMARY KEY, parent_id VARCHAR(30), {substr});")
    
    rows = list(map(tuple,precomputed_rows.values()))
    
    substr = ["?"] * 52
    substr = ",".join(substr)

    cursor.executemany(f"INSERT INTO precomputed VALUES (?,?,{substr});", rows)
    conn.commit()
    cursor.close()

    s3_client = boto3.client('s3')
    if OUT_BUCKET_NAME not in s3_client.list_buckets():
        s3_client.create_bucket(Bucket=OUT_BUCKET_NAME)
        s3_client.upload_file(f"tmp/{date.today()}.db", OUT_BUCKET_NAME, f"{date.today()}.db")
    
    # else:
    #     s3_client.download_file(OUT_BUCKET_NAME, FILE_NAME, FILE_NAME)

    #     conn = sqlite3.connect(FILE_NAME)
    #     cursor = conn.cursor()

    #     res = cursor.execute("SELECT node_id FROM precomputed;")
    #     id_set = set(map(lambda x: x[0], res.fetchall()))

    #     for key, val in precomputed_rows.items():
    #         if key in id_set:
    #             substr = []
    #             for year in range(2010, 2023):
    #                 substr.append(f"pick_rate_numerator{year} = pick_rate_numerator{year} + ?")
    #                 substr.append(f"pick_rate_denominator{year} = pick_rate_denominator{year} + ?")
    #                 substr.append(f"win_rate_numerator{year} = win_rate_numerator{year} + ?")
    #                 substr.append(f"win_rate_denominator{year} = win_rate_denominator{year} + ?")
    #             substr = ", ".join(substr)
    #             cursor.execute(f"UPDATE precomputed SET {substr} WHERE node_id = ?", [key] + val[2:])
    #         else:
    #             substr = ",".join(["?"] * 52)
    #             cursor.execute(f"INSERT INTO precomputed VALUES (?,?,{substr});", val)
    #     conn.commit()
    #     cursor.close()

    #     s3_client.upload_file(FILE_NAME, OUT_BUCKET_NAME, FILE_NAME)
            

if __name__ == "__main__":
    precompute()