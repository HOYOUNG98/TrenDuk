from typing import List
from pandas.core.frame import DataFrame

from pandas.io.parsers import read_csv


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
                {"color": color, "move": x + reflect(y)})

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
                "_id": current_id,
                "parent": parent_id,
                "depth": iteration,
                "move": move["move"],
                "color": move["color"],
                "data": [{"date": game["date"], "win": win, "link": game["link"]}]
            }
        else:
            nodes[current_id]["data"].append(
                {"date": game["date"], "win": win, "link": game["link"]})

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

    # original_df = read_csv('cyberoro_games.csv')

    # for i in range(original_df.shape[0]):
    #     moves = original_df.iloc[i]["moves"].split(";")
    #     for corner in assortCorners(moves):
    #         print(corner)
    #         print()
    #     break

    test_df = read_csv('cyberoro_games.csv')
    test_df = test_df[(test_df["result"] != "")]
    nodes = {}
    print(test_df.shape)
    for index, row in test_df.iterrows():
        game = row.to_dict()
        moves = game["moves"].split(";")
        print(game["result"], index)
        corners = assortCorners(moves)
        for corner in corners:
            nodes = createNodes(corner, game, nodes)

    nodes_df = DataFrame(nodes.values())
    nodes_df['data_length'] = nodes_df['data'].str.len()
    print(nodes_df.sort_values(by=['depth', 'move', 'color']))
    new_df = nodes_df[(nodes_df["depth"] == 0)]
    print(new_df["move"].unique())
    print(nodes_df.shape)
