from scraper import Scraper
from mongoengine import *

from model import Gibo, Node
from analyze import *
import config

# Seems like under 2014 doesn't work really well
CHOSEN_PAGES = [1, 2, 3, 4, 5, 75, 76, 78, 79, 80, 155, 156, 157, 158, 159, 250, 251, 252, 253, 254, 300, 301, 302, 303, 304, 350, 351, 352, 353, 354, 400, 401, 402, 403, 404 ]

if __name__ == "__main__":

    connect('GiboDB', host=config.DB_URL)

    print("EXTRACT - extract games from website")
    print("ANALYZE - analyze extracted games")
    print()

    command = input("COMMAND: ")

    if command == "EXTRACT":
        links = []
        for page in CHOSEN_PAGES:
            Scraper.scrape_links_page(links, 1, page)
        for link in links:
            info = Scraper.scrape_game(link)
            if info == None:
                continue
            giboInstance = Gibo(giboName=info[0],
                                giboDate=info[1],
                                giboLocation=info[2],
                                giboMinutes=info[3],
                                giboSeconds=info[4],
                                giboTimeCount=info[5],
                                giboKomi=info[6],
                                giboResult=info[7],
                                giboBlackPlayerName=info[8],
                                giboBlackPlayerRank=info[9],
                                giboWhitePlayerName=info[10],
                                giboWhitePlayerRank=info[11],
                                giboMoves=info[13],
                                giboLink=info[14])

            # duplicateGibo = Gibo.objects(giboLink=info[14])

            # if len(duplicateGibo) != 0:
            #     break
            giboInstance.save()

    if command == "ANALYZE":

        parent = Node.objects(root=True)

        if len(parent) == 0:
            root = Node(root=True)
            root.save()
            parent = root
        else:
            parent = parent[0]

        gibos = Gibo.objects(analyzed=False)

        for i in range(len(gibos)):
            corners = assortCorners(gibos[i].giboMoves)
            for corner in corners:
                updateTree(corner, parent, gibos[i])
                parent = Node.objects(root=True)
                parent = parent[0]

            # print(i, "/", len(gibos))
            # game analyzed
            # gibo.update(analyzed=True)
