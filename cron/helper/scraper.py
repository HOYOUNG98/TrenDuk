# library imports
import requests
import bs4
from pymongo import MongoClient

# local imports
from helper.database import findGiboByFilter

"""
    In cyberoro page, we can mainly consider 2 types of links
    1. page that contains links of games (10 games max)
    2. page that shows the game
    This file will mainly have functions working around these two types of pages.
"""

client = MongoClient("mongodb+srv://kevin4163:ghdi4163@trenduk.sucyo.mongodb.net/trenduk?retryWrites=true&w=majority")
gibo = client["trenduk"]["gibo"]


def request(link):
    response = requests.get(link)
    decoded_content = bs4.BeautifulSoup(response.content.decode("euc-kr", "replace"), "html.parser")
    return decoded_content


"""
    Find (at max) 10 links inside content. Check for duplicates from database.
    If duplicate found, return with False as second value
"""


def parse_links(content):
    link_divs = content.findAll(class_="board_pd", align="left")

    links = []
    for div in link_divs:
        link = div.find("a")["href"][21:-2]
        link = link[1 : (link.find(",") - 1)]

        results = findGiboByFilter({"link": link})
        if results.count() > 0:
            return links, False
        links.append(link)

    return links, True


def parse_game(content, link):
    content = content.prettify()
    end_semi_colon = content.find(";")

    if end_semi_colon == -1:
        return None

    info = content[1:end_semi_colon]
    info = info.replace("[", ":").replace("\r\n", "")
    split_info = info.split("]")

    gibo = {"time": {}, "blackPlayer": {}, "whitePlayer": {}, "moves": [], "link": link}
    for category in split_info:
        if len(category) <= 2:
            continue

        field = category[:2]
        if field == "TE":
            gibo["title"] = category[3:]
        elif field == "RD":
            gibo["date"] = category[3:]
        elif field == "PC":
            gibo["location"] = category[3:]
        elif field == "TM":
            gibo["time"]["given"] = category[3:]
        elif field == "LT":
            gibo["time"]["seconds"] = category[3:]
        elif field == "LC":
            gibo["time"]["count"] = category[3:]
        elif field == "KO":
            gibo["komi"] = category[3:]
        elif field == "RE":
            gibo["result"] = category[3:]
        elif field == "PB":
            gibo["blackPlayer"]["name"] = category[3:]
        elif field == "BR":
            gibo["blackPlayer"]["rank"] = category[3:]
        elif field == "PW":
            gibo["whitePlayer"]["name"] = category[3:]
        elif field == "WR":
            gibo["whitePlayer"]["rank"] = category[3:]
        elif field == "HD":
            gibo["handicap"] = category[3:]
        else:
            print("Undefined category:", category)

    moves = content[end_semi_colon + 1 :]
    end_parenthesis = moves.find(")")

    if end_parenthesis == -1:
        return None

    moves = moves[:end_parenthesis]
    moves = moves.replace("[", "").replace("]", "")
    split_moves = moves.split(";")

    for split_move in split_moves:
        move = {}
        move["color"] = split_move[:1]
        move["move"] = split_move[1:]
        gibo["moves"].append(move)

    if (
        "아마" in gibo["blackPlayer"]["name"]
        or "아마" in gibo["whitePlayer"]["name"]
        or "아마" in gibo["blackPlayer"]["rank"]
        or "아마" in gibo["whitePlayer"]["rank"]
    ):
        return None

    gibo["link"] = link
    gibo["_id"] = hash(
        (gibo["date"], gibo["result"], gibo["title"], gibo["blackPlayer"]["name"], gibo["whitePlayer"]["name"])
    )

    return gibo


if __name__ == "__main__":
    link = "https://www.cyberoro.com/bcast/gibo.oro?param=1&div=1&Tdiv=B&Sdiv=2&pageNo=1&blockNo=1"
    print("??")
    content = request(link)
    links = parse_links(content)
    for link in links:
        content = request(link)
        gibo = parse_game(content, link)
