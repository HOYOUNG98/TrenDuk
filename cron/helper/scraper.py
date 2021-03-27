# library imports
import requests
import bs4
from pymongo import MongoClient

'''
    In cyberoro page, we can mainly consider 2 types of links
    1. page that contains links of games (10 games max)
    2. page that shows the game
    This file will mainly have functions working around these two types of pages.
'''

client = MongoClient(
    "mongodb+srv://kevin4163:ghdi4163@trenduk.sucyo.mongodb.net/trenduk?retryWrites=true&w=majority")
gibo = client['trenduk']['gibo']


def request(link):
    response = requests.get(link)
    decoded_content = bs4.BeautifulSoup(
        response.content.decode('euc-kr', 'replace'), "html.parser")
    return decoded_content


'''
    Find (at max) 10 links inside content. Check for duplicates from database.
    If duplicate found, return with False as second value
'''


def parse_links(content):
    link_divs = content.findAll(class_="board_pd", align="left")

    links = []
    for div in link_divs:
        link = div.find("a")["href"][21:-2]
        link = link[1:(link.find(",")-1)]

        count = gibo.count_documents({"link": link})
        if count > 0:
            return links, False
        links.append(link)

    return links, True


def parse_game(content):
    content = content.prettify()
    end_semi_colon = content.find(";")

    if end_semi_colon == -1:
        return None

    info = content[1:end_semi_colon]
    info = info.replace("[", ":").replace("\r\n", "")
    split_info = info.split("]")

    gibo = {"Time": {}, "BlackPlayer": {}, "WhitePlayer": {}, "Moves": []}
    for category in split_info:
        if len(category) <= 2:
            continue

        field = category[:2]
        if field == "TE":
            gibo["Title"] = category[3:]
        elif field == "RD":
            gibo["Date"] = category[3:]
        elif field == "PC":
            gibo["Location"] = category[3:]
        elif field == "TM":
            gibo["Time"]["Given"] = category[3:]
        elif field == "LT":
            gibo["Time"]["Seconds"] = category[3:]
        elif field == "LC":
            gibo["Time"]["Count"] = category[3:]
        elif field == "KO":
            gibo["Komi"] = category[3:]
        elif field == "RE":
            gibo["Result"] = category[3:]
        elif field == "PB":
            gibo["BlackPlayer"]["Name"] = category[3:]
        elif field == "BR":
            gibo["BlackPlayer"]["Rank"] = category[3:]
        elif field == "PW":
            gibo["WhitePlayer"]["Name"] = category[3:]
        elif field == "WR":
            gibo["WhitePlayer"]["Rank"] = category[3:]
        elif field == "HD":
            gibo["Handicap"] = category[3:]
        else:
            print("Undefined category:", category)

    moves = content[end_semi_colon+1:]
    end_parenthesis = moves.index(")")

    if end_parenthesis == -1:
        return None

    moves = moves[:end_parenthesis]
    moves = moves.replace("[", "").replace("]", "")
    split_moves = moves.split(";")

    for split_move in split_moves:
        move = {}
        move["Color"] = split_move[:1]
        move["Move"] = split_move[1:]
        gibo["Moves"].append(move)

    return None


if __name__ == "__main__":
    link = "https://www.cyberoro.com/bcast/gibo.oro?param=1&div=1&Tdiv=B&Sdiv=2&pageNo=1&blockNo=1"
    print("??")
    content = request(link)
    links = parse_links(content)
    for link in links:
        content = request(link)
        parse_game(content)
