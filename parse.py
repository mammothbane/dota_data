import csv
import json
import os

data = {}
for match in os.listdir('data'):
    with open('data/' + match) as f:
        data[match] = json.load(f)

out = {}

for match, info in data.items():
    first_blood = [elem for elem in info['objectives'] if elem['type'] == 'CHAT_MESSAGE_FIRSTBLOOD']

    if first_blood:
        radiant_first_blood = first_blood[0]['player_slot'] < 100
    else:
        radiant_first_blood = None

    towers = [elem for elem in info['objectives'] if elem['type'] == 'CHAT_MESSAGE_TOWER_KILL']

    if not towers:
        first_tower_radiant = None
    else:
        first_tower_radiant = min(towers, key=lambda x: x['time'])['team'] == 2

    rosh_killed = [elem for elem in info['objectives'] if elem['type'] == 'CHAT_MESSAGE_ROSHAN_KILL']
    radiant_rosh_lead = 0

    if not rosh_killed:
        radiant_first_rosh = None
        killer = None
    else:
        killer = min(rosh_killed, key=lambda x: x['time'])['team']
        for elem in rosh_killed:
            diff = 1
            if elem['team'] != 2:
                diff = -1

            radiant_rosh_lead += diff

    radiant_first_rosh = killer == 2

    def kill_diff_at_time(tm):
        radiant_lead = 0
        for player in info['players']:
            if 'kills_log' not in player:
                continue
            kills = len([elem for elem in player['kills_log'] if elem['time'] < tm])
            if not player['isRadiant']:
                kills = -kills
            radiant_lead += kills

        return radiant_lead

    def lh_diff_at_time(tm):
        radiant_lead = 0
        for player in info['players']:
            if len(player['lh_t']) <= tm:
                return None

            amt = player['lh_t'][tm]
            if not player['isRadiant']:
                amt = -amt

            radiant_lead += amt
        return radiant_lead

    dire_obs_count = sum([player['observer_uses'] for player in info['players'] if not player['isRadiant'] and 'observer_uses' in player])
    radiant_obs_count = sum([player['observer_uses'] for player in info['players'] if player['isRadiant'] and 'observer_uses' in player])

    dire_sen_count = sum([player['sentry_uses'] for player in info['players'] if not player['isRadiant'] and 'sentry_uses' in player])
    radiant_sen_count = sum([player['sentry_uses'] for player in info['players'] if player['isRadiant'] and 'sentry_uses' in player])

    radiant_win = info['players'][0]['radiant_win']

    adv = info['radiant_gold_adv']
    radiantLeads = info['radiant_gold_adv'][10]

    out[match] = {
        'winner': 'radiant' if radiant_win else 'dire',
        'dire_obs': dire_obs_count,
        'radiant_obs': radiant_obs_count,
        'first_roshan': None if not killer else ('radiant' if radiant_first_rosh else 'dire'),
        'radiant_gl_10': adv[10] if len(adv) > 10 else None,
        'radiant_gl_20': adv[20] if len(adv) > 20 else None,
        'radiant_gl_30': adv[30] if len(adv) > 30 else None,
        'first_blood': None if not first_blood else ('radiant' if radiant_first_blood else 'dire'),
        'first_tower': None if not towers else ('radiant' if first_tower_radiant else 'dire'),
        'radiant_kl_10': kill_diff_at_time(60*10),
        'radiant_kl_20': kill_diff_at_time(60*20),
        'radiant_kl_30': kill_diff_at_time(60*30),
        'radiant_sen': radiant_sen_count,
        'dire_sen': dire_sen_count,
        'radiant_lhl_10': lh_diff_at_time(9),
        'radiant_lhl_20': lh_diff_at_time(19),
        'radiant_lhl_30': lh_diff_at_time(29),
        'game_duration_sec': info['duration'],
        'radiant_team': info['radiant_team']['name'] if 'radiant_team' in info else None,
        'dire_team': info['dire_team']['name'] if 'dire_team' in info else None,
        'radiant_rosh_lead': radiant_rosh_lead
    }


with open('ti6.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, ['winner', 'dire_obs', 'radiant_obs', 'first_roshan', 'radiant_gl_10', 'radiant_gl_20',
                           'radiant_gl_30', 'first_blood', 'first_tower',
                           'radiant_kl_10', 'radiant_kl_20', 'radiant_kl_30',
                           'radiant_sen', 'dire_sen',
                           'radiant_lhl_10', 'radiant_lhl_20', 'radiant_lhl_30',
                           'game_duration_sec', 'radiant_team', 'dire_team',
                           'radiant_rosh_lead'])
    w.writeheader()
    w.writerows(out.values())
