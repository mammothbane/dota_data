import os
import json
import csv

data = {}
for match in os.listdir('../replays/data'):
    with open('../replays/data/' + match) as f:
        data[match] = json.load(f)

out = {}

for match, info in data.items():
    rosh_killed = [elem for elem in info['objectives'] if elem['type'] == 'CHAT_MESSAGE_ROSHAN_KILL']

    if rosh_killed == []:
        radiant_first_rosh = None
        killer = None
    else:
        killer = min(rosh_killed, key=lambda x: x['time'])['team']

    radiant_first_rosh = killer == 2

    dire_obs_count = sum([player['observer_uses'] for player in info['players'] if not player['isRadiant'] and player['observer_uses']])
    radiant_obs_count = sum([player['observer_uses'] for player in info['players'] if player['isRadiant'] and player['observer_uses']])

    radiant_win = info['players'][0]['radiant_win']

    adv = info['radiant_gold_adv']
    radiantLeads = info['radiant_gold_adv'][10]

    out[match] = {
        'winner': 'radiant' if radiant_win else 'dire',
        'dire_obs': dire_obs_count,
        'radiant_obs': radiant_obs_count,
        'first_roshan': None if not killer else ('radiant' if radiant_first_rosh else 'dire'),
        'gl_10': adv[10] if len(adv) > 10 else None,
        'gl_20': adv[20] if len(adv) > 20 else None,
        'gl_30': adv[30] if len(adv) > 30 else None
    }

with open('ti6.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, ['winner', 'dire_obs', 'radiant_obs', 'first_roshan', 'gl_10', 'gl_20', 'gl_30'])
    w.writeheader()
    w.writerows(out.values())
