from pymongo import MongoClient
from bson.objectid import ObjectId

RECURSION_DEPTH = 8

client = MongoClient("mongodb+srv://kevin4163:ghdi4163@trenduk.sucyo.mongodb.net/trenduk?retryWrites=true&w=majority")
gibo = client["trenduk"]["gibo"]


def assort_corners(moves):
    top_right = []
    top_left = []
    bottom_right = []
    bottom_left = []

    for i in range(len(moves)):
        x = moves[i]["move"][0]
        y = moves[i]["move"][1]

        if (
            len(top_right) == RECURSION_DEPTH
            and len(top_left) == RECURSION_DEPTH
            and len(bottom_right) == RECURSION_DEPTH
            and len(bottom_left) == RECURSION_DEPTH
        ):
            break

        if x <= "j" and y <= "j" and len(top_left) < RECURSION_DEPTH:
            top_left.append({"color": moves[i]["color"], "move": reflect(x) + y})
        if x >= "j" and y >= "j" and len(bottom_right) < RECURSION_DEPTH:
            bottom_right.append({"color": moves[i]["color"], "move": x + reflect(y)})
        if x <= "j" and y >= "j" and len(top_right) < RECURSION_DEPTH:
            top_right.append({"color": moves[i]["color"], "move": reflect(x) + reflect(y)})
        if x >= "j" and y <= "j" and len(bottom_left) < RECURSION_DEPTH:
            bottom_left.append({"color": moves[i]["color"], "move": x + reflect(y)})

    all_corners = [top_left, top_right, bottom_left, bottom_right]

    for i in range(4):
        corner = all_corners[i]
        reflected = False
        for j in range(RECURSION_DEPTH):
            move = corner[j]

            if not move:
                continue

            x = move["move"][0]
            y = move["move"][1]
            if reflected:
                all_corners[i][j] = {"color": moves[i]["color"], "move": reflect(y) + reflect(x)}
            else:

                if j == 0 and reflect(x) < y:
                    reflected = True

                if j == 1 and reflect(x) > y:
                    reflected = True

                if j == 2 and reflect(x) < y:
                    reflected = True

    return all_corners


def build_tree(root, moves, gibo):

    if len(moves) == 0:
        return root

    move = moves[0]
    win = 0
    lose = 0

    if move["color"] == check_winner(gibo["result"]):
        win += 1
    else:
        lose += 1

    matching_child = {}
    for child in root["children"]:
        if child["color"] == move["color"] and child["move"] == move["move"]:
            matching_child = child

    if not matching_child:
        new_node = {
            "root": False,
            "parent": root,
            "depth": RECURSION_DEPTH - len(moves) + 1,
            "children": [],
            "move": move["move"],
            "color": move["color"],
            "games": [gibo["_id"]],
            "yearlyStat": [{"year": gibo["date"][:4], "count": 1, "win": win, "lose": lose}],
            "count": 1,
        }

        root["children"].append(new_node)
        build_tree(new_node, moves[1:], gibo)
    else:
        found = False
        for yearly_stat in matching_child["yearlyStat"]:
            if yearly_stat["year"] == gibo["date"][:4]:
                yearly_stat["count"] += 1
                yearly_stat["win"] += win
                yearly_stat["lose"] += lose
                found = True

        if not found:
            matching_child["yearlyStat"].append(
                {"year": gibo["date"][:4], "count": 1, "win": win, "lose": lose,}
            )
        if "count" in root.keys():
            root["count"] += 1
        build_tree(matching_child, moves[1:], gibo)

    return root


def tree_to_list(root, assignedID, parentID=None):
    childrenID = []
    return_value = []

    for child in root["children"]:
        newID = hash((child["move"], child["color"], parentID))
        childrenID.append(newID)
        output = tree_to_list(child, newID, assignedID)
        return_value = return_value + output

    if root["root"]:
        return_value.append({"_id": assignedID, "root": True, "children": childrenID})
    else:
        return_value.append(
            {
                "_id": assignedID,
                "root": False,
                "move": root["move"],
                "parent": parentID,
                "children": childrenID,
                "depth": root["depth"],
                "games": root["games"],
                "yearlyStat": root["yearlyStat"],
                "count": root["count"],
                "color": root["color"],
            }
        )

    return return_value


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


def check_winner(result_string):
    if result_string.find("흑") == -1:
        return "W"
    else:
        return "B"
