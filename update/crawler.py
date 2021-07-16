from typing import List
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame, read_csv
import csv


def request(link: str):
    response = requests.get(link)
    decoded_content = BeautifulSoup(
        response.content.decode("euc-kr", "replace"), "html.parser")
    return decoded_content


def parsePage(link: str, latest_link: str = None):
    content: BeautifulSoup = request(link)
    link_divs = content.find_all(class_="board_pd", align="left")

    links = []
    for div in link_divs:
        link = div.find("a")["href"][21:-2]
        link = link[1: (link.find(",") - 1)]

        if link == latest_link:
            break

        links.append(link)
    return links


def parseGame(link: str):
    content = request(link).prettify()
    end_semi_colon = content.find(";")

    # some files don't have ; ending
    if end_semi_colon == -1:
        return None

    info = content[1:end_semi_colon]
    info = info.replace("[", ":").replace("\r\n", "")
    split_info = info.split("]")

    gibo = {}
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
            gibo["time_given"] = category[3:]
        elif field == "LT":
            gibo["time_seconds"] = category[3:]
        elif field == "LC":
            gibo["time_count"] = category[3:]
        elif field == "KO":
            gibo["komi"] = category[3:]
        elif field == "RE":
            gibo["result"] = category[3:]
        elif field == "PB":
            # Amateur games are ignored
            if "아마" in category[3:]:
                return None
            gibo["black_player_name"] = category[3:]
        elif field == "BR":
            # Amateur games are ignored
            if "아마" in category[3:]:
                return None
            gibo["black_player_rank"] = category[3:]
        elif field == "PW":
            # Amateur games are ignored
            if "아마" in category[3:]:
                return None
            gibo["white_player_name"] = category[3:]
        elif field == "WR":
            # Amateur games are ignored
            if "아마" in category[3:]:
                return None
            gibo["white_player_rank"] = category[3:]
        elif field == "HD":
            gibo["handicap"] = category[3:]
        else:
            print("Undefined category:", category)

    moves = content[end_semi_colon + 1:]
    end_parenthesis = moves.find(")")

    # Some files are missing end parenthesis
    if end_parenthesis == -1:
        return None

    gibo["link"] = link
    moves = moves[:end_parenthesis]
    moves = moves.replace("[", "").replace("]", "")
    gibo["moves"] = moves

    return gibo


if __name__ == "__main__":
    original_df = read_csv('cyberoro.csv')
    latest_link = original_df.iloc[0]["link"]
    gibo_list = []
    for page in range(1, 800):
        link = "https://www.cyberoro.com/bcast/gibo.oro?param=1&div=1&Tdiv=B&Sdiv=2&pageNo={0}&blockNo=1".format(
            page)
        links = parsePage(link, latest_link)

        for link in links:
            gibo = parseGame(link)
            if gibo:
                gibo_list.append(gibo)
            else:
                continue

        # Prevent duplicates
        if len(links) != 20:
            break

    print(len(gibo_list))
    gibo_df = DataFrame(gibo_list)

    # fetch original csv to preprend DF
    gibo_df.append(original_df, sort=False)

    gibo_df.to_csv("cyberoro.csv", index=False,
                   encoding="utf-8-sig", quotechar='"', quoting=csv.QUOTE_ALL)