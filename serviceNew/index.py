from scraper.scraper import scrapeGamePage, scrapeLinksPage

if __name__ == "__main__":
    links = scrapeLinksPage(pageOptions=(1, 1))

    parsedData = scrapeGamePage(links[0])
