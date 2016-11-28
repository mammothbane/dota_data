import json
import os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode

import backoff
import requests

QUERY = '''
SELECT match_id, leagueid
FROM matches
WHERE leagueid = 4664
'''

req = requests.get('http://api.opendota.com/api/explorer?{}'.format(urlencode({'sql': QUERY})))

if req.status_code != 200:
    raise Exception('unable to retrieve data from api')

items = os.listdir('data')
data = [elem['match_id'] for elem in req.json()['rows'] if str(elem['match_id']) not in items]
API_ROOT = 'https://api.opendota.com/api/matches/{}'


def write_out(fut):
    res = fut.result().json()

    with open('data/%s' % res['match_id'], 'w') as f:
        json.dump(res, f)


def predicate_log(details):
    print("Backing off {wait:0.1f} seconds afters {tries} tries ".format(**details))


@backoff.on_predicate(backoff.expo, lambda x: x.status_code != 200 or 'error' in x.json(), on_backoff=predicate_log)
def retrieve(elem):
    return requests.get(API_ROOT.format(elem))


with ThreadPoolExecutor(30) as tx:
    futures = [tx.submit(retrieve, elem) for elem in data]
    futures = [tx.submit(write_out, fut) for fut in futures]
    [fut.result() for fut in futures]
