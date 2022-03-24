import sys
import sqlite3
import json

conn = sqlite3.connect("../main.db", check_same_thread=False)
cursor = conn.cursor()

move = 'pp'
color = 'B'
sequence_depth = 1

node_id = f'{move}{color}{sequence_depth}rootroot0root'

query = f'''
        WITH children AS (
            SELECT child_id
            FROM node 
                JOIN is_child ON node.node_id = is_child.parent_id
            WHERE parent_id = '{node_id}'
        ),

        total AS (
            SELECT Substr(game.datetime, 0, 5) as year, COUNT(*) AS total
            FROM node_game
                JOIN children ON node_game.node_id = children.child_id
                JOIN game ON node_game.game_id = game.game_id
            GROUP BY Substr(game.datetime, 0, 5)
        ),

        game_ AS (
            SELECT *,
                CASE 
                    WHEN Substr(game.result, 0, 2) = '{color}' THEN 1
                    WHEN Substr(game.result, 0, 2) <> '{color}' THEN 0
                END AS win
            FROM game
        ),

        res AS (
            SELECT children.child_id as move, Substr(game_.datetime, 0, 5) as year, CAST(SUM(win) AS FLOAT) / CAST(COUNT(*) AS FLOAT) as win_rate, COUNT(*) as sub_total
            FROM node_game
                JOIN game_ ON game_.game_id = node_game.game_id
                JOIN children ON children.child_id = node_game.node_id
            GROUP BY children.child_id, Substr(game_.datetime, 0, 5)
            HAVING sub_total > 5
        )

        SELECT Substr(move, 0, 5) as move, res.year, res.win_rate, CAST(sub_total AS FLOAT) / CAST(total.total as FLOAT) as pick_rate
        FROM res LEFT JOIN total ON res.year = total.year;
        '''

res = cursor.execute(query).fetchall()

# year from 2000 to 2022
years, colors = list({val[0] for val in res}), ['B', 'W']
yearly: dict[str, dict[str, float]] = {key1: {key2: 0 for key2 in colors} for key1 in years}

moves = list({val[0] for val in res})

pick_rates = {key: [0 for _ in range(23)] for key in moves}
win_rates = {key: [0 for _ in range(23)] for key in moves}
for move_, year_, win_rate_, pick_rate_ in res:
    if 0 <= int(year_) - 2000 <= 22:
        pick_rates[move_][int(year_) - 2000] = pick_rate_
        win_rates[move_][int(year_) - 2000] = win_rate_

print(json.dumps({"pick_rate": pick_rates, "win_rate": win_rates}))

sys.stdout.flush()