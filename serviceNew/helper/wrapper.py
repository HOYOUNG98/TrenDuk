# library imports
from mongoengine import *
from multiprocessing import Pool

# local imports
from scraper.scraper import scrapeGamePage, scrapeLinksPage
from helper.analyzer import assortCorners, updateTree
from model.Gibo import Gibo
from model.Node import Node
from constant import DB_URL


def scrapeAndSave():

    for page in range(1, 437):
        links = scrapeLinksPage(pageOptions=(1, page))

        documentList = []
        for link in links:
            parsedData = scrapeGamePage(link)

            # If data is none
            if parsedData == None:
                continue

            # If data is already in DB
            if Gibo.objects(giboLink=parsedData[14]).count() != 0:
                print("Msg: DUPLICATE FOUND", parsedData[14])
                continue

            # If year of game is lower than 2013 omit
            if parsedData[1][0:4] < '2014':
                print("Msg: OBSOLETE DATA FOUND", parsedData[1])
                continue

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
                                giboWhitePlayerRank=parsedData[12],
                                giboMoves=parsedData[13],
                                giboLink=parsedData[14])

            documentList.append(giboDocument)

        if len(documentList) != 0:
            response = Gibo.objects.insert(documentList)
            print("{} Documents from page {} inserted".format(
                len(documentList), page))


def analyzeGames():
    root = Node(root=True)
    root.save()

    allGames = Gibo.objects()

    root = Node.objects(root=True).first()
    counter = 1
    for gibo in allGames:
        corners = assortCorners(gibo.giboMoves)
        for corner in corners:
            updateTree(corner, root, gibo)

        print("Completed Analysis for {}/{} games".format(counter, len(allGames)))
        counter += 1
