from pymongo import MongoClient
from bson.objectid import ObjectId

RECURSION_DEPTH = 8


def assort_corners(moves):
    top_right = []
    top_left = []
    bottom_right = []
    bottom_left = []

    for i in range(len(moves)):
        x = moves[i]["Move"][0]
        y = moves[i]["Move"][1]

        if (
            len(top_right) == RECURSION_DEPTH
            and len(top_left) == RECURSION_DEPTH
            and len(bottom_right) == RECURSION_DEPTH
            and len(bottom_left) == RECURSION_DEPTH
        ):
            break

        if x <= "j" and y <= "j" and len(top_left) < 8:
            top_left.append({"Color": moves[i]["Color"], "Move": reflect(x) + y})
        if x >= "j" and y >= "j" and len(bottom_right) < 8:
            bottom_right.append({"Color": moves[i]["Color"], "Move": x + reflect(y)})
        if x <= "j" and y >= "j" and len(top_right) < 8:
            top_right.append({"Color": moves[i]["Color"], "Move": reflect(x) + reflect(y)})
        if x >= "j" and y <= "j" and len(bottom_left) < 8:
            bottom_left.append({"Color": moves[i]["Color"], "Move": x + reflect(y)})

    all_corners = [top_left, top_right, bottom_left, bottom_right]

    for i in range(4):
        corner = all_corners[i]
        reflected = False
        for j in range(RECURSION_DEPTH):
            move = corner[j]

            if not move:
                continue

            x = move["Move"][0]
            y = move["Move"][1]
            if reflected:
                all_corners[i][j] = {"Color": moves[i]["Color"], "Move": reflect(y) + reflect(x)}
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

    if move["Color"] == check_winner(gibo["Result"]):
        win += 1
    else:
        lose += 1

    matching_child = {}
    for child in root["Children"]:
        if child["Color"] == move["Color"] and child["Move"] == move["Move"]:
            matching_child = child

    if not matching_child:
        new_node = {
            "Root": False,
            "Parent": root,
            "Move": move["Move"],
            "Color": move["Color"],
            "Games": [gibo["ID"]],
            "YearlyStat": [{"Year": gibo["Date"][:4], "Count": 1, "Win": win, "Lose": lose}],
            "Count": 1,
        }

        root["Children"].append(new_node)
        root = build_tree(new_node, moves[1:], gibo)
    else:
        found = False
        for yearly_stat in matching_child["YearlyStat"]:
            if yearly_stat["Year"] == gibo["Date"][:4]:
                yearly_stat["Count"] += 1
                yearly_stat["Win"] += win
                yearly_stat["Lose"] += lose
                found = True

        if not found:
            matching_child["YearlyStat"].append(
                {"Year": gibo["Date"][:4], "Count": 1, "Win": win, "Lose": lose,}
            )
        root["Count"] += 1
        root = build_tree(matching_child, moves[1:], gibo)

    return root


def tree_to_list(root, parentID, assignedID):
    childrenID = []
    return_value = []

    for child in root["Children"]:
        newID = ObjectId()
        childrenID.append(newID)
        output = tree_to_list(child, assignedID, newID)
        return_value.append(output)

    if root["Root"]:
        return_value.append({"ID": assignedID, "Root": True, "Children": childrenID})
    else:
        return_value.append(
            {
                "ID": assignedID,
                "Root": False,
                "Move": root["Move"],
                "Root": root["Root"],
                "Parent": parentID,
                "Children": childrenID,
                "YearlyStat": root["YearlyStat"],
                "Count": root["Count"],
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
