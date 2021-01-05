import requests
import bs4


def getURL(url_no, page_no):
    if url_no == 1:
        return "https://www.cyberoro.com/bcast/gibo.oro?param=1&div=1&Tdiv=B&Sdiv=2&pageNo={0}&blockNo=1".format(
            page_no)
    elif url_no == 2:
        return "https://www.cyberoro.com/bcast/gibo.oro?param=1&div=2&Tdiv=B&Sdiv=4&pageNo={0}&blockNo=1".format(
            page_no)
    elif url_no == 3:
        return "https://www.cyberoro.com/bcast/gibo.oro?param=1&div=3&Tdiv=B&Sdiv=5&pageNo={0}&blockNo=1".format(
            page_no)
    else:
        return EnvironmentError  # Just using some default error class for now


# TODO: endless fetching -> through all pages
# TODO: duplicate data found?
def scrapeLinksPage(pageOptions=(1, 1), rolling=False):

    url = getURL(pageOptions[0], pageOptions[1])
    page = requests.get(url)
    pageContent = bs4.BeautifulSoup(page.content.decode(
        'euc-kr', 'replace'), "html.parser")
    linkContainers = pageContent.findAll(class_="board_pd", align="left")

    # Loop through each table data and extract the link
    links = []
    for linkContainer in linkContainers:

        link = linkContainer.find("a")["href"]
        link = link[21:-2]
        commaIndex = link.find(",")
        link = link[1:commaIndex-1]

        links.append(link)

    return links


# Extract data from gibo link
# Return the Class instance for parsed data
def scrapeGamePage(link):
    linkRequest = requests.get(link)
    soup = bs4.BeautifulSoup(
        linkRequest.content.decode("euc-kr", "replace"), "html.parser").prettify()

    # Ad hoc of checking if value(sgf data) is successfully received
    # In some cases, the cyberoro server has not succesfully fetched the game from server
    if soup[0] != "(":
        print("INVALID DATA RECEIVED:", soup)
        return None

    finalData = []

    record = False
    buildWord = ""
    for character in soup:
        # Moves start here
        if character == ";":
            break

        # The word I want to store starts here
        if character == "[":
            record = True
            continue

        # The word I want to store ends here
        if character == "]":
            record = False
            finalData.append(buildWord)
            buildWord = ""

        if record:
            buildWord += character

    moves = []
    rawMoves = soup[soup.find(";")+1:]

    for move in rawMoves.split(";"):
        moves.append((move[0], move[2:4]))

    finalData.append(moves)
    finalData.append(link)

    # Check if finalData is not fulfilled
    if len(finalData) != 15:
        print("NOT ENOUGH DATA:", finalData)
        return None

    return finalData
