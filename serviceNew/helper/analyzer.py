from model.Node import Node

REFLECT_OBJECT = {
    "s": "a", "r": "b", "q": "c", "p": "d", "o": "e", "n": "f", "m": "g", "l": "h", "k": "i", "j": "j",
    "a": "s", "b": "r", "c": "q", "d": "p", "e": "o", "f": "n", "g": "m", "h": "l", "i": "k"}


def assortCorners(moves):
    topRight = []
    topLeft = []
    bottomRight = []
    bottomLeft = []

    for i in range(len(moves)):
        x = moves[i][1][0]
        y = moves[i][1][1]

        if x <= "j" and y <= "j" and len(topLeft) < 8:
            topLeft.append((moves[i][0], REFLECT_OBJECT[x] + y))
        if x >= "j" and y >= "j" and len(bottomRight) < 8:
            bottomRight.append(
                (moves[i][0], x + REFLECT_OBJECT[y]))
        if x <= "j" and y >= "j" and len(topRight) < 8:
            topRight.append(
                (moves[i][0], REFLECT_OBJECT[x] + REFLECT_OBJECT[y]))
        if x >= "j" and y <= "j" and len(bottomLeft) < 8:
            bottomLeft.append(moves[i])

    return [topLeft, topRight, bottomLeft, bottomRight]


def updateTree(moveList, root, game):
    iteration = 0
    reflected = False
    currentNode = root
    for (color, move) in moveList:

        # Guide for first iteration
        if (iteration % 2) == 0 and not reflected and REFLECT_OBJECT[move[0]] < move[1]:
            reflected = True

        # Guide for second iteration
        # Cases when first move have equal x and y values
        if (iteration % 2) == 1 and not reflected and REFLECT_OBJECT[move[0]] > move[1]:
            reflected = True

        if reflected:
            move = REFLECT_OBJECT[move[1]] + REFLECT_OBJECT[move[0]]

        # Check if child already exists
        child = None
        child = Node.objects(id__in=currentNode.children,
                             color=color, move=move).first()

        if child:
            # update data
            tempDict = child.yearPickCount
            if game.giboDate[0:4] in child.yearPickCount.keys():
                tempDict[game.giboDate[0:4]] += 1
            else:
                tempDict[game.giboDate[0:4]] = 1

            child.games.append(game.id),
            child.yearPickCount = tempDict
            child.save()

            currentNode = child

        else:
            # Create new node
            pickDict = {game.giboDate[0:4]: 1}
            child = Node(parent=currentNode.id, children=[],
                         move=move, color=color, games=[game.id], yearPickCount=pickDict)
            child = child.save()

            # Update parent node
            currentNode.children.append(child.id)
            currentNode.save()

            # Next parent node in loop to be current child
            currentNode = child

        iteration += 1
