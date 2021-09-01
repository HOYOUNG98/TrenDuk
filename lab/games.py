from lab.config import URI
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from pandas import DataFrame
from tqdm import tqdm
from pymongo import MongoClient
import time

START_YEAR = 2021
NUM_YEAR = 16


def initialFetch():
    driver = webdriver.Safari()
    driver.get("http://m.baduk.or.kr/record/C01_list.asp#none")

    for i in range(NUM_YEAR):
        select = Select(driver.find_element_by_id("s_yyyy"))
        select.select_by_visible_text(str(START_YEAR - i) + " 년")

        select = Select(driver.find_element_by_id("s_win_appy_yn"))
        select.select_by_visible_text("공식")

        button = driver.find_element_by_id("btn_search").click()
        time.sleep(1)

        total = driver.find_element_by_id("lblTotal")
        total = int(total.text.replace(",", ""))

        count = len(driver.find_elements_by_class_name("winner"))

        pbar = tqdm(total=total)
        print("Year {0}".format(START_YEAR - i))
        while count <= total:
            button = driver.find_element_by_id("AddList")
            button.click()
            time.sleep(2)

            old_count = count
            count = len(driver.find_elements_by_class_name("winner"))
            pbar.update(count - old_count)
        pbar.close()

        elems = driver.find_elements_by_class_name("tb-date")
        dates = [elem.text for elem in elems]

        last_date = dates[0]
        for j in range(len(dates)):
            if dates[j] == "\xa0":
                dates[j] = last_date
            else:
                last_date = dates[j]

        elems = driver.find_elements_by_class_name("winner")
        winners = [elem.text for elem in elems]

        elems = driver.find_elements_by_class_name("loser")
        losers = [elem.text for elem in elems]

        data = []
        columns = ["date", "winner", "loser"]
        for j in range(len(dates)):
            data.append([dates[j], winners[j], losers[j]])
        games_df = DataFrame(data, columns=columns)
        data = games_df.to_dict(orient="records")

        # Insert into database
        client = MongoClient(URI)
        collection = client["games"]["{0}_games".format(START_YEAR - i)]
        collection.insert_many(data)

        driver.refresh()

    driver.close()
