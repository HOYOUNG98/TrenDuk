# library imports
import requests
import bs4

# local imports


class Scraper:

    # TODO: have this in constant file
    @staticmethod
    def get_URL(url_no, page_no):
        MAIN_URL = ""
        if url_no == 1:
            MAIN_URL = "https://www.cyberoro.com/bcast/gibo.oro?param=1&div=1&Tdiv=B&Sdiv=2&pageNo={0}&blockNo=1".format(
                page_no)
        elif url_no == 2:
            MAIN_URL = "https://www.cyberoro.com/bcast/gibo.oro?param=1&div=2&Tdiv=B&Sdiv=4&pageNo={0}&blockNo=1".format(
                page_no)
        elif url_no == 3:
            MAIN_URL = "https://www.cyberoro.com/bcast/gibo.oro?param=1&div=3&Tdiv=B&Sdiv=5&pageNo={0}&blockNo=1".format(
                page_no)
        else:
            return EnvironmentError  # Just using some default error class for now

        return MAIN_URL

    @staticmethod
    # Scrapes links of gibos in a single page and stores it to links variable passed by as parameter. 1 page = 10 games
    # If last page (game number < 10) return False, else True
    def scrape_links_page(links, url_no, page_no):

        main_url = Scraper.get_URL(url_no, page_no)
        main_page = requests.get(main_url)
        soup = bs4.BeautifulSoup(main_page.content.decode(
            'euc-kr', 'replace'), "html.parser")
        results = soup.findAll(class_="board_pd", align="left")

        # Loop through each table data and extract the link
        for table_data in results:

            link_caller = table_data.find("a")["href"]
            link_parse = link_caller[21:-2]
            comma = link_parse.find(",")
            link = link_parse[1:comma-1]
            # cyberoro_id = link_parse[comma+2:-1]

            # if duplicate found in database stop looking for values

            links.append(link)

        if len(results) == 20:
            return True
        else:
            return False

    @staticmethod
    # Extract data from gibo link
    # Return the Class instance for parsed data
    def scrape_game(link):
        individual_game = requests.get(link)
        soup = bs4.BeautifulSoup(
            individual_game.content.decode("euc-kr", "replace"), "html.parser").prettify()

        record = False
        info = []
        partial_info = ""
        print(soup)
        for character in soup:
            if character == ";":
                break

            if character == "[":
                record = True
                continue

            if character == "]":
                record = False
                info.append(partial_info)
                partial_info = ""

            if record:
                partial_info += character

        # This gets rid of useless data if fetched more - Some dataset has more fields then usual
        # while len(info) > 13:
        #    info.pop()
        ###########################
        if len(info) != 13:
            return None
        ###########################

        moves = soup[soup.find(";")+1:]
        moves_parsed = []
        for move in moves.split(";"):
            moves_parsed.append((move[0], move[2:4]))

        info.append(moves_parsed)
        info.append(link)

        return info
