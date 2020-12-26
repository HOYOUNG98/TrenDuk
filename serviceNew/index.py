# library imports
from mongoengine import *

# local imports
from scraper.scraper import scrapeGamePage, scrapeLinksPage
from model.Gibo import Gibo
from model.Node import Node
from helper.analyzer import assortCorners, updateTree
from constant import DB_URL

# test
import timeit

if __name__ == "__main__":

    db = connect('GiboDB', host=DB_URL)
    Gibo.objects().delete()
    Node.objects().delete()

    for page in ([1]):
        links = scrapeLinksPage(pageOptions=(1, 1))
        documentList = []
        for link in links:
            parsedData = scrapeGamePage(link)
            # If data is none
            if parsedData == None:
                continue

            # If data is already in DB
            if Gibo.objects(giboLink=parsedData[14]).count() != 0:
                print("DUPLICATE FOUND")
                break

            giboDocument = Gibo(giboName=parsedData[0],
                                giboDate=parsedData[1],
                                giboLocation=parsedData[2],
                                giboMinutes=parsedData[3],
                                giboSeconds=parsedData[4],
                                giboTimeCount=parsedData[5],
                                giboKomi=parsedData[6],
                                giboResult=parsedData[7],
                                giboBlackPlayerName=parsedData[8],
                                giboBlackPlayerRank=parsedData[9],
                                giboWhitePlayerName=parsedData[10],
                                giboWhitePlayerRank=parsedData[11],
                                giboMoves=parsedData[13],
                                giboLink=parsedData[14])

            documentList.append(giboDocument)

        if len(documentList) != 0:
            response = Gibo.objects.insert(documentList)

        root = Node.objects(root=True)

        if len(root) == 0:
            root = Node(root=True)
            root.save()
        else:
            root = root[0]

        for document in documentList:
            corners = assortCorners(document.giboMoves)
            for corner in corners:
                start = timeit.default_timer()

                updateTree(corner, root, document)

                stop = timeit.default_timer()

                print('Time: ', stop - start)
                root.reload()
