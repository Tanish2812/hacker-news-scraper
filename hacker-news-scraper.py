import csv
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException, NoSuchElementException, StaleElementReferenceException)

options = Options()
# options.add_argument("--headless=new")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36")
options.add_argument("--blink-settings=imagesEnabled=false")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)
driver.maximize_window()

def safe_text(parent, by, value):
    found = parent.find_elements(by, value)
    return found[0].text.strip() if found else ""

def safe_attr(parent, by, value, attr):
    found = parent.find_elements(by, value)
    return found[0].get_attribute(attr) if found else ""

def to_int(text):
    value = re.search(r"\d+", text)
    return int(value.group()) if value else 0


records = []
skipped = []
page = 1


while True:
    url = f"https://news.ycombinator.com/news?p={page}"

    driver.get(url)
    time.sleep(random.uniform(1, 3))

    try:
        stories = wait.until(
            EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, ".athing.submission"))
        )
    except TimeoutException:
        break

    for i, story in enumerate(stories):
        try:
            rank = safe_text(story, By.CSS_SELECTOR, ".rank").strip('.')
            title = safe_text(story, By.CSS_SELECTOR, ".titleline>a")
            points = safe_text(story, By.XPATH, "./following-sibling::tr//span[@class='score']")
            author = safe_text(story, By.XPATH, "./following-sibling::tr//a[@class='hnuser']")
            comments = safe_text(story, By.XPATH, "./following-sibling::tr//span[@class='subline']/a[last()]")
            link = safe_attr(story, By.CSS_SELECTOR, ".titleline>a", "href")

            points = to_int(points)
            comments = to_int(comments)

            records.append({
                "Rank": rank,
                "Title": title,
                "Points": points,
                "Author": author,
                "Comments": comments,
                "Link": link
            })

        except (NoSuchElementException, StaleElementReferenceException):
            skipped.append(f"Page: {page}, Item: {i+1}")
            continue

    page += 1

    if page > 3:
        break

with open("stories.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Rank", "Title", "Points", "Author", "Comments", "Link"])
    writer.writeheader()
    writer.writerows(records)

print(f"Saved: {len(records)} records, Skipped:{len(skipped)}")

driver.quit()