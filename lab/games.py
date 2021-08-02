from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pandas import DataFrame
from selenium.webdriver.support import expected_conditions as EC

import time
import csv

START_YEAR = 2006
NUM_YEAR = 1

if __name__ == "__main__":
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

        counter = 0
        while counter < ((total // 10) + 10):
            button = driver.find_element_by_id("AddList")
            try:
                button.click()
                time.sleep(0.5)
                counter += 1
            except ElementNotInteractableException:
                time.sleep(0.5)
                counter -= 1

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
        games_df.to_csv(
            "./data/games/{0}_games.csv".format(START_YEAR - i),
            index=False,
            encoding="utf-8-sig",
            quotechar='"',
            quoting=csv.QUOTE_ALL,
        )

    driver.close()
