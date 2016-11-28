import os
import json

data = {f: json.load(f) for f in os.listdir('../replays/data')}
out = {}

for match, info in data.items():
    rosh_killed = [elem for elem in data['objectives'] if elem['type'] == 'CHAT_MESSAGE_ROSHAN_KILL']
    killer = min(rosh_killed, key=lambda x: x['time'])['player_slot']

    radiant_first_rosh = False
    for player in data['players']:
        if player['player_slot'] == killer:
            radiant_first_rosh = player['isRadiant']

    dire_obs_count = sum([player['obs_placed'] for player in data['players'] if not player['isRadiant']])
    radiant_obs_count = sum([player['obs_placed'] for player in data['players'] if player['isRadiant']])

    radiant_win = data['radiant_win']

    radiantLeads = data['radiant_gold_adv']