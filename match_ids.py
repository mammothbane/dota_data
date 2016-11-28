import re
from concurrent.futures import ThreadPoolExecutor

import requests

match_ids = []
link = re.compile(r'/matches/([0-9]+)')

league = '4664'
pages = 20

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'


def retrieve_page(page):
    ids = []

    req = requests.get('https://www.dotabuff.com/esports/leagues/%s/matches?page=%s' % (league, page),
                       headers={'user-agent': USER_AGENT})

    if req.status_code != 200:
        raise Exception('failed retrieval')

    position = 0
    while True:
        match = link.search(req.text, pos=position)
        if match is None:
            break

        ids.append(match.groups()[0])
        position = match.end()

    return ids

with ThreadPoolExecutor(pages) as tx:
    futures = []
    for i in range(pages):
        futures.append(tx.submit(retrieve_page, i))

    for f in futures:
        match_ids += f.result()

with open('match_ids', 'w') as f:
    for elem in match_ids:
        f.write(elem + '\n')
