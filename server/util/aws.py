from __future__ import annotations
import zipfile

import boto3
import os
import sys
import csv

from parser_ import Parser
from type_ import Node, Game
from tqdm import tqdm
from io import BytesIO

BUCKET_NAME = "trenduk-zip"


if not os.environ.get('PYTHONHASHSEED'):
    os.environ['PYTHONHASHSEED'] = '0'
    os.execv(sys.executable, ['python3'] + sys.argv)

client = boto3.client('s3')


objects = client.list_objects(Bucket=BUCKET_NAME)


nodes: dict[str, 'Node'] = {}
games: dict[str, 'Game'] = {}

for obj in objects["Contents"]:
    key = obj["Key"]

    res = client.get_object(Bucket=BUCKET_NAME, Key=key)
    buffer = BytesIO(res['Body'].read())
    zipped = zipfile.ZipFile(buffer)

    for file in tqdm(zipped.namelist()):
        with zipped.open(file, "r") as f_in:
            game_info, game_moves = Parser.read_bytes(f_in.read())
            game_instance = Game(game_info)

            games[game_instance.id] = game_instance

            for sequence in Parser.divide_sequences(game_moves):

                if not sequence:
                    continue

                sequence_dict = Parser.parse_sequence(sequence, game_info)

                for key, val in sequence_dict.items():
                    if key in nodes:
                        nodes[key].mergeNode(val)
                    else:
                        nodes[key] = val

with open("../data/nodes.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(Node.keys())
    for obj in tqdm(nodes.values()):
        writer.writerow(obj.__dict__.values())


with open("../data/games.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(Game.keys())
    for obj in tqdm(games.values()):
        writer.writerow(obj.__dict__.values())
