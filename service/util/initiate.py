from __future__ import annotations
from re import A
import zipfile

import boto3
import os
import sys
import csv

from parser_ import Parser
from type_ import Node, Game
from tqdm import tqdm
from io import BytesIO
import psycopg2
import random

# S3
BUCKET_NAME = "trenduk-zip"
FILE_NAME = "initiate.zip"

# RDS
ENDPOINT = "trenduk-database.c0uhqsts6mxo.us-east-1.rds.amazonaws.com"
PORT = "5432"
DBNAME = "postgres"
USER = "postgres"


def export_hash_seed():
    if not os.environ.get('PYTHONHASHSEED'):
        os.environ['PYTHONHASHSEED'] = '0'
        os.execv(sys.executable, ['python3'] + sys.argv)


def load_from_s3():
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
    buffer = BytesIO(response['Body'].read())
    zipped = zipfile.ZipFile(buffer)

    games, nodes = {}, {}
    print(len(zipped.namelist()))
    for file in tqdm(random.sample(zipped.namelist(), 10000)):
        with zipped.open(file, "r") as f_in:
            game_info, game_moves = Parser.read_bytes(f_in.read())
            game_instance = Game(game_info)

            games[game_instance.id] = game_instance

            # There are four corners
            for sequence in Parser.divide_sequences(game_moves):

                # There may be invalid sequences
                if not sequence:
                    continue

                sequence_dict = Parser.parse_sequence(sequence, game_info)

                for key, val in sequence_dict.items():
                    if key in nodes:
                        nodes[key].mergeNode(val)
                    else:
                        nodes[key] = val

    return games, nodes


def save_to_rds(games, nodes):
    sql = ""

    sql += "CREATE TABLE node (node_id VARCHAR(50) PRIMARY KEY, move VARCHAR(2) NOT NULL, color VARCHAR(1) NOT NULL, sequence_depth INT); \n"
    sql += "CREATE TABLE game (game_id VARCHAR(50) PRIMARY KEY, datetime VARCHAR(50), event VARCHAR(100), round VARCHAR(100), black_player VARCHAR(50), black_rank VARCHAR(10), white_player VARCHAR(50), white_rank VARCHAR(10), komi VARCHAR(5), result VARCHAR(10)); \n"
    sql += "CREATE TABLE node_game (node_id VARCHAR(50) NOT NULL, game_id VARCHAR(50) NOT NULL, game_depth INTEGER, FOREIGN KEY (node_id) references node(node_id), FOREIGN KEY (game_id) references game(game_id), PRIMARY KEY (node_id, game_id, game_depth)); \n"
    sql += "CREATE TABLE is_child (parent_id VARCHAR(50) NOT NULL, child_id VARCHAR(50) NOT NULL, FOREIGN KEY (parent_id) references node(node_id), FOREIGN KEY (child_id) references node(node_id), PRIMARY KEY (parent_id, child_id)); \n"

    for val in tqdm(games.values()):
        sql += f"INSERT INTO game VALUES ('{val.id}', '{val.datetime}', '{val.event}', '{val.round}', '{val.black_player}', '{val.black_rank}', '{val.white_player}', '{val.white_rank}', '{val.komi}', '{val.result}'); \n"

    for val in tqdm(nodes.values()):
        sql += f"INSERT INTO node VALUES ('{val.id}', '{val.move}', '{val.color}', {val.sequence_depth}); \n"

    for val in tqdm(nodes.values()):
        for game_id, game_depth in val.games:
            sql += f"INSERT INTO node_game VALUES ('{val.id}', '{game_id}', '{game_depth}'); \n"

        for child in val.children:
            sql += f"INSERT INTO is_child VALUES ('{val.id}', '{child}'); \n"

    conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME,
                            user=USER, password="ghdi4163", sslrootcert="SSLCERTIFICATE", **{
                                "keepalives": 1,
                                "keepalives_idle": 3000,
                                "keepalives_interval": 5,
                                "keepalives_count": 5,
                            })

    cur = conn.cursor()

    cur.execute('''
            DROP TABLE IF EXISTS node_game;
            DROP TABLE IF EXISTS is_child;
            DROP TABLE IF EXISTS node;
            DROP TABLE IF EXISTS game;
        ''')

    cur.execute(sql)

    conn.commit()
    print("done!")


def main():
    games, nodes = load_from_s3()
    save_to_rds(games, nodes)


if __name__ == "__main__":
    export_hash_seed()
    main()
