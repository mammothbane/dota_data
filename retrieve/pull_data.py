import requests
import json
import backoff
import os

from concurrent.futures import ThreadPoolExecutor

with open('match_ids') as f:
    data = f.readlines()

data = [elem for elem in data if str(elem).strip() not in os.listdir('../replays/data')]
API_ROOT = 'https://api.opendota.com/api/matches/{}'

print(len(data))

def write_out(fut):
    res = fut.result().json()

    if 'match_id' not in res:
        print("HELP")
        print(res)
        exit()

    with open('../replays/data/%s' % res['match_id'], 'w') as f:
        json.dump({key: res[key] for key in ['objectives', 'players', 'radiant_gold_adv']}, f)


def predicate_log(details):
    print("Backing off {wait:0.1f} seconds afters {tries} tries ".format(**details))


@backoff.on_predicate(backoff.expo, lambda x: x.status_code != 200 or 'error' in x.json(), on_backoff=predicate_log)
def retrieve(elem):
    return requests.get(API_ROOT.format(elem))


with ThreadPoolExecutor(30) as tx:
    futures = [tx.submit(retrieve, elem) for elem in data]

    print('all requests submitted')

    futures = [tx.submit(write_out, fut) for fut in futures]
    [fut.result() for fut in futures]
