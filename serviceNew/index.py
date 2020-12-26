from scraper.scraper import scrapeGamePage, scrapeLinksPage
from model.Gibo import Gibo
from model.Node import Node

if __name__ == "__main__":
    links = scrapeLinksPage(pageOptions=(1, 1))

    parsedData = scrapeGamePage(links[0])
    

    #connect('GiboDB', host=config.DB_URL)
