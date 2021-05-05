from bson.objectid import ObjectId

RECURSION_DEPTH = 16


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
        for j in range(len(corner)):
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
    win = True

    if move["color"] != check_winner(gibo["result"]):
        win = False

    # Find matching child from current node
    matching_child = {}
    for child in root["children"]:
        if child["color"] == move["color"] and child["move"] == move["move"]:
            matching_child = child

    # If no matching child found, create a new node
    if not matching_child:
        new_child = {
            "children": [],
            "parent": root,
            "depth": RECURSION_DEPTH - len(moves) + 1,
            "move": move["move"],
            "color": move["color"],
            "data": [{"date": gibo["date"], "win": win, "gibo": gibo["_id"]}],
        }
        root["children"].append(new_child)

        build_tree(new_child, moves[1:], gibo)

    # If matching child found, only add new data
    else:
        matching_child["data"].append(
            {
                "date": gibo["date"],
                "win": win,
                "gibo": gibo["_id"],
            }
        )
        build_tree(matching_child, moves[1:], gibo)

    return root


def tree_to_list(root, parent_id=None, current_id=hash("root_hash")):
    return_value = []

    # Traverse through children
    children_id_list = []
    for child in root["children"]:
        child_id = hash((child["move"], child["color"], current_id))
        children_id_list.append(child_id)

        output = tree_to_list(child, current_id, child_id)
        return_value = return_value + output

    if root["depth"] == 0:
        return_value.append({"_id": current_id, "children": children_id_list, "depth": root["depth"]})
    else:
        return_value.append(
            {
                "_id": current_id,
                "parent": parent_id,
                "children": children_id_list,
                "depth": root["depth"],
                "move": root["move"],
                "color": root["color"],
                "data": root["data"],
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
