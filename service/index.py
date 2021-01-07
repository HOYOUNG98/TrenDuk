# library imports
from mongoengine import *

# local imports
from constant import DB_URL
from helper.wrapper import scrapeAndSave, analyzeGames

# test
import timeit

if __name__ == "__main__":

    db = connect('GiboDB', host=DB_URL)

    db.copyDatabase("test", "production")

    Node

    # scrapeAndSave()
    # analyzeGames()
