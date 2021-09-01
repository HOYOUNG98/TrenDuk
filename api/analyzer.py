# library imports
from typing import List
from pandas.core.frame import DataFrame
from pandas.io.parsers import read_csv
import csv
from os import listdir


RECURSION_DEPTH = 16


def assortCorners(moves: List[str]):
    top_right = []
    top_left = []
    bottom_right = []
    bottom_left = []

    for i in range(len(moves)):
        color = moves[i][0]
        x = moves[i][1]
        y = moves[i][2]

        if (
            len(top_right) == RECURSION_DEPTH
            and len(top_left) == RECURSION_DEPTH
            and len(bottom_right) == RECURSION_DEPTH
            and len(bottom_left) == RECURSION_DEPTH
        ):
            break

        if x <= "j" and y <= "j" and len(top_left) < RECURSION_DEPTH:
            top_left.append(
                {"color": color, "move": reflect(x) + y})
        if x >= "j" and y >= "j" and len(bottom_right) < RECURSION_DEPTH:
            bottom_right.append(
                {"color": color, "move": x + reflect(y)})
        if x <= "j" and y >= "j" and len(top_right) < RECURSION_DEPTH:
            top_right.append(
                {"color": color, "move": reflect(x) + reflect(y)})
        if x >= "j" and y <= "j" and len(bottom_left) < RECURSION_DEPTH:
            bottom_left.append(
                {"color": color, "move": x + y})

    all_corners = [top_left, top_right, bottom_left, bottom_right]

    for i in range(4):
        corner = all_corners[i]
        reflected = False
        for j in range(len(corner)):
            move = corner[j]

            if not move:
                continue

            color = move["color"]
            x = move["move"][0]
            y = move["move"][1]
            if reflected:
                all_corners[i][j] = {"color": color,
                                     "move": reflect(y) + reflect(x)}
            else:

                if j == 0 and reflect(x) < y:
                    reflected = True

                if j == 1 and reflect(x) > y:
                    reflected = True

                if j == 2 and reflect(x) < y:
                    reflected = True

    return all_corners


def createNodes(moves, game, nodes={}):
    parent_id = "root"
    for iteration, move in enumerate(moves):
        win = True if move["color"] != checkWinner(game["result"]) else False
        current_id = hash((parent_id, move["move"], move["color"]))

        if current_id not in nodes:
            nodes[current_id] = {
                '_id': current_id,
                "parent": parent_id,
                "depth": iteration,
                "move": move["move"],
                'color': move["color"],
                "num_data": 1,
                "num_win": 1,
                "link": [game["link"]],
            }
        else:
            nodes[current_id]["num_win"] += 1 if win else 0
            nodes[current_id]["num_data"] += 1
            nodes[current_id]["link"].append(game["link"])

        parent_id = current_id

    return nodes


def mergeNodes(nodes1, nodes2):
    return_nodes = {}
    intersection = nodes1.keys() & nodes2.keys()
    nodes1_keys = [k for k in nodes1 if k not in intersection]
    nodes2_keys = [k for k in nodes2 if k not in intersection]

    for k in nodes1_keys:
        return_nodes[k] = nodes1[k]

    for k in nodes2_keys:
        return_nodes[k] = nodes2[k]

    for k in intersection:
        nodes1[k]["data"] = nodes1[k]["data"] + nodes2[k]["data"]
        return_nodes[k] = nodes1[k]

    return return_nodes


def reflect(character):
    return {
        "s": "a",
        "r": "b",
        "q": "c",
        "p": "d",
        "o": "e",
        "n": "f",
        "m": "g",
        "l": "h",
        "k": "i",
        "j": "j",
        "a": "s",
        "b": "r",
        "c": "q",
        "d": "p",
        "e": "o",
        "f": "n",
        "g": "m",
        "h": "l",
        "i": "k",
    }[character]


def checkWinner(result: str):
    # check wrong typings
    if type(result) != str:
        return False
    if result.find("흑") == -1:
        return "W"
    else:
        return "B"


def dictListFind(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1


if __name__ == "__main__":

    # original_df = read_csv("cyberoro_games.csv")

    # for i in range(original_df.shape[0]):
    #     moves = original_df.iloc[i]["moves"].split(";")
    #     for corner in assortCorners(moves):
    #         print(corner)
    #         print()
    #     break

    filenames = listdir("./data/games")
    print(filenames)
    for file in filenames:
        year = file[:4]
        current_csv = read_csv("./data/games/"+file)
        current_csv = current_csv[(current_csv["result"] != "")]
        nodes = {}
        for index, row in current_csv.iterrows():
            game = row.to_dict()
            moves = game["moves"].split(";")
            corners = assortCorners(moves)
            for corner in corners:
                nodes = createNodes(corner, game, nodes)

        nodes_df = DataFrame(nodes.values())
        nodes_df.sort_values(by=["depth", "move", "color"])
        nodes_df.to_csv("./data/moves/{}_cyberoro_nodes.csv".format(year), index=False,
                        encoding="utf-8-sig", quotechar='"', quoting=csv.QUOTE_ALL)
