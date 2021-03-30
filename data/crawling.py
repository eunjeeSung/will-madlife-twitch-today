import csv
import random
import re
import time
from urllib import request

import html5lib
from bs4 import BeautifulSoup
from tqdm import tqdm

BASE_URL = "https://tgd.kr/s/lol_madlife"
CATEGORY_URL_SUFFIX = 'category=18356422'
MAX_PAGE = 11


def is_notice(soup):
    span = soup.find("span", "category")
    if span:
        return span.get_text() == "방송 공지"
    return False

def is_off_notice(soup):
    title = soup.find("a").get_text()
    off_strs = ["휴방", "쉽", "쉬어"]
    return any(off_str in title for off_str in off_strs)

def soup_to_date(soup):
    timestamp = soup.find("div", {"class": "list-time"}).get_text()
    timestamp = re.findall(r'[0-9][0-9]\-[0-9][0-9]', timestamp)[0]
    date_str = timestamp.split('-')
    month, day = int(date_str[0]), int(date_str[1])
    return month, day


if __name__ == "__main__":
    # Supply request with headers
    hdr = { 'User-Agent' : "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0" }
    
    # Store dates
    dates = []

    # Iterate through the category pages
    for i in tqdm(range(MAX_PAGE)):        
        # Get html
        url = f'{BASE_URL}/page/{i+1}?{CATEGORY_URL_SUFFIX}'
        req = request.Request(url, headers=hdr)
        with request.urlopen(req) as f:
            html = f.read().decode('utf-8')

        # Parse with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        notices = soup.find_all("div", {"class": "article-list-row"})
        dates += [soup_to_date(notice) for notice in notices if is_off_notice(notice)]

        time.sleep(1 + random.uniform(-0.5, 1.5))

    with open('notice_dates.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for date in dates:
            writer.writerow(date)