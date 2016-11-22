import requests
import bz2
from concurrent.futures import ThreadPoolExecutor


match_ids = []

with open('match_ids') as f:
    while True:
        id = f.readline().strip()
        if not id:
            break
        match_ids.append(id)

def download(id):
    print('retrieving url for match %s' % id)

    req = requests.get('https://api.opendota.com/api/matches/%s' % id,
                       headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'})

    if req.status_code != 200:
        raise Exception('failed fetching match %s with status %s' % (id, req.status_code))

    js = req.json()
    if not 'replay_url' in js:
        raise Exception('no replay url available for replay %s' % id)

    print('downloading match %s' % id)
    replay = requests.get(js['replay_url'])
    data = bz2.decompress(replay.content)
    with open('replays/%s.dem' % id, 'wb') as f:
        f.write(data)

with ThreadPoolExecutor(50) as tx:
    futures = []

    for match in match_ids:
        futures.append(tx.submit(download, match))

    for future in futures:
        future.result()
