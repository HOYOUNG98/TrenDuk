from model import Node

reflect_object = {
    "s": "a", "r": "b", "q": "c", "p": "d", "o": "e", "n": "f", "m": "g", "l": "h", "k": "i", "j": "j",
    "a": "s", "b": "r", "c": "q", "d": "p", "e": "o", "f": "n", "g": "m", "h": "l", "i": "k"}


def assortCorners(moves):
    top_right = []
    top_left = []
    bottom_right = []
    bottom_left = []

    for i in range(len(moves)):
        x = moves[i][1][0]
        y = moves[i][1][1]

        if x <= "j" and y <= "j" and len(top_left) < 8:
            top_left.append((moves[i][0], reflect_object[x] + y))
        if x >= "j" and y >= "j" and len(bottom_right) < 8:
            bottom_right.append(
                (moves[i][0], x + reflect_object[y]))
        if x <= "j" and y >= "j" and len(top_right) < 8:
            top_right.append(
                (moves[i][0], reflect_object[x] + reflect_object[y]))
        if x >= "j" and y <= "j" and len(bottom_left) < 8:
            bottom_left.append(moves[i])

    return [top_left, top_right, bottom_left, bottom_right]


def updateTree(moves, tree, game):
    iteration = 0
    reflected = False
    for (color, move) in moves[0:]:

        # Guide for first iteration
        if (iteration % 2) == 0 and not reflected and reflect_object[move[0]] < move[1]:
            reflected = True

        # Guide for second iteration
        # Cases when first move have equal x and y values
        if (iteration % 2) == 1 and not reflected and reflect_object[move[0]] > move[1]:
            reflected = True

        if reflected:
            move = reflect_object[move[1]] + reflect_object[move[0]]

        # Check if child already exists
        children = Node.objects(id__in=tree.childrenID)
        child = None
        for x in children:
            if x.color == color and x.move == move:
                child = x

        if child:
            # update data
            tempDict = child.yearPickCount
            if game.giboDate[0:4] in child.yearPickCount.keys():
                tempDict[game.giboDate[0:4]] += 1
            else:
                tempDict[game.giboDate[0:4]] = 1
            child.update(push__games=game.id,
                         yearPickCount=tempDict)

            tree = child

        else:
            # Create new node
            pickDict = {game.giboDate[0:4]: 1}
            child = Node(parentID=tree.id, childrenID=[],
                         move=move, color=color, games=[game.id], yearPickCount=pickDict)
            child = child.save()

            # Update parent node
            tree.update(push__childrenID=child.id)

            # Next parent node in loop to be current child
            tree = child

        iteration += 1
