__author__ = 'damyers'

import re
import requests
import json
import time
import datetime
from lxml import html


def main():
    """
    Scrape application listings from appdb.winehq and store them in an json object.
    :return: json application listing
    """
    winehq_file = 'winehq.json'
    ratings = ['Platinum', 'Gold']
    main_url = "https://appdb.winehq.org/objectManager.php?bIsQueue=false&bIsRejected=false&sClass=application&sTitle=Browse+Applications&iItemsPerPage=200&iPage=1&iappVersion-ratingOp0=5&sappVersion-ratingData0={rating}%3Cbr%20/%3E&sOrderBy=appId&bAscending=true&iItemsPerPage=200&iPage={page}"
    page_regex = re.compile("Page 1 of ([0-9]*)")
    results = {}
    results['date'] = str(datetime.datetime.now())

    for rating in ratings:
        time.sleep(2)
        first_page = requests.get(main_url.format(rating=rating, page=1))
        first_tree = html.fromstring(first_page.text)
        page_range = [result.group(1) for item in [b.text_content() for b in first_tree.xpath('//b')] for result in [page_regex.search(item)] if result][0]
        items = [td.text_content() for td in first_tree.xpath('//td')]

        for pos in range(3, len(items), 3):
            results[items[pos + 1]] = {"app": items[pos], "description": items[pos + 2], "rating": rating}

        for page_number in range(int(page_range)):
            time.sleep(2)
            page = requests.get(main_url.format(rating=rating, page=page_number))
            tree = html.fromstring(page.text)
            items = [td.text_content() for td in tree.xpath('//td')]

            for pos in range(3, len(items), 3):
                results[items[pos + 1]] = {"app": items[pos], "description": items[pos + 2], "rating": rating}

    with open(winehq_file, 'w') as winehq_raw:
        json.dump(results, winehq_raw)

if __name__ == "__main__":
    main()