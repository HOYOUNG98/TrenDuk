from selenium import webdriver
from pandas import DataFrame
import time
import csv

START_YEAR = 2021
NUM_YEAR = 16

if __name__ == "__main__":
    driver = webdriver.Safari()
    driver.get("http://m.baduk.or.kr/record/C04_list.asp#none")

    # Traverse through all 15 years
    for i in range(NUM_YEAR):
        # Check all months
        for j in range(12):
            buttons = driver.find_elements_by_tag_name("button")
            buttons[j + 3].click()
            time.sleep(0.5)

            # Check for emtpy page
            elem = driver.find_elements_by_tag_name("td")
            if elem[0].text == "리스트가 없습니다.":
                continue

            # Fetch data from page
            # Find and click more button
            elems = driver.find_elements_by_tag_name("td")
            counter = 0
            while elems[-1].text != "리스트가 없습니다." and counter < 11:
                find_button = driver.find_element_by_id("AddList")
                find_button.click()
                time.sleep(0.5)
                elems = driver.find_elements_by_tag_name("td")
                counter += 1

            # Find all cell values - 5 cells per player
            # Last element says end of list, so remove
            elems = driver.find_elements_by_tag_name("td")
            if len(elems) % 5 != 0:
                elems = elems[:-1]
            elems = list(map(lambda x: x.text, elems))

            # Split list into chunks of list of 5 values
            data = [elems[i : i + 5] for i in range(0, len(elems), 5)]

            # Create dataframe using the values crawled
            columns = ["rank", "name", "rating", "rank_change", "rating_change"]
            rating_df = DataFrame(data, columns=columns)
            rating_df.to_csv(
                "./data/rating/{0}_{1}_ratings.csv".format(START_YEAR - i, j + 1),
                index=False,
                encoding="utf-8-sig",
                quotechar='"',
                quoting=csv.QUOTE_ALL,
            )

        # Second button in page goes back a year
        driver.find_elements_by_tag_name("button")[1].click()
        time.sleep(0.5)

    driver.close()
