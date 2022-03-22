from fastapi import FastAPI

import sqlite3

app = FastAPI()
conn = sqlite3.connect("../main.db", check_same_thread=False)
cursor = conn.cursor()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/move/")
def get_move(color: str, move: str, sequence_depth: int):
    node_id = f'{move}{color}{sequence_depth}'

    query = f'''
            SELECT Substr(game.datetime, 0, 5), Substr(game.result, 0, 2), COUNT(*)
            FROM game
            WHERE game_id IN (SELECT node_game.game_id
                FROM node_game 
                    NATURAL JOIN node
                WHERE node_game.node_id = '{node_id}')
            GROUP BY Substr(game.datetime, 0, 5), Substr(game.result, 0, 2);
            '''

    res = cursor.execute(query).fetchall()

    years, colors = list({val[0] for val in res}), ['B', 'W']
    yearly: dict[str, dict[str, float]] = {key1: {key2: 0 for key2 in colors} for key1 in years}

    for year_, color_, count_ in res:
        yearly[year_][color_] = count_

    for key, val in yearly.items():
        total = sum(val.values())
        yearly[key]['win_rate'] = yearly[key][color] / total

    return yearly

    # calculate win rate, pick rate
 