from argparse import ArgumentParser
from collections import Counter
from datetime import datetime

from jsonlines import open
from tqdm import tqdm

US_STATES = {
    'alabama',
    'alaska',
    'arizona',
    'arkansas',
    'california',
    'colorado',
    'connecticut',
    'delaware',
    'florida',
    'georgia',
    'hawaii',
    'idaho',
    'illinois',
    'indiana',
    'iowa',
    'kansas',
    'kentucky',
    'louisiana',
    'maine',
    'maryland',
    'massachusetts',
    'michigan',
    'minnesota',
    'mississippi',
    'missouri',
    'montana',
    'nebraska',
    'nevada',
    'new_hampshire',
    'new_jersey',
    'new_mexico',
    'new_york',
    'north_carolina',
    'north_dakota',
    'ohio',
    'oklahoma',
    'oregon',
    'pennsylvania',
    'rhode_island',
    'south_carolina',
    'south_dakota',
    'tennessee',
    'texas',
    'utah',
    'vermont',
    'virginia',
    'washington',
    'west_virginia',
    'wisconsin',
    'wyoming',
}

# Experiment 1

SOUTH = {  # Region 3 (South)
    # Division 5 (South Atlantic) without DC (as per Nisbett & Cohen)
    'delaware', 'florida', 'georgia', 'maryland', 'north_carolina',
    'south_carolina', 'virginia', 'west_virginia',

    # Division 6 (East South Central)
    'kentucky', 'mississippi', 'tennessee', 'alabama',

    # Division 7 (West South Central)
    'arkansas', 'louisiana', 'oklahoma', 'texas',
}
NORTH = {
    'california',
    'nevada',
    'wyoming',
    'washington',
    'kansas',
    'new_jersey',
    'new_york',
    'colorado',
    'south_dakota',
    'maine',
    'new_mexico',
    'north_dakota',
    'arizona',
    'oregon',
    'wisconsin',
    'minnesota',
    'rhode_island',
    'missouri',
    'vermont',
    'montana',
    'pennsylvania',
    'connecticut',
    'idaho',
    'utah',
    'michigan',
    'illinois',
    'new_hampshire',
    'ohio',
    'nebraska',
    'iowa',
    'massachusetts',
    'indiana',
}

# # Experiment 2
# 
# SOUTH = {  # Region 3 (South)
#     # Division 5 (South Atlantic) without DC, MD, and DE (as per Nisbett &
#     # Cohen)
#     'florida', 'georgia', 'north_carolina',
#     'south_carolina', 'virginia', 'west_virginia',
# 
#     # Division 6 (East South Central)
#     'kentucky', 'mississippi', 'tennessee', 'alabama',
# 
#     # Division 7 (West South Central)
#     'arkansas', 'louisiana', 'oklahoma', 'texas',
# 
#     # Southernness-index of 25 or more (as per Nisbett & Cohen)
#     'arizona', 'new_mexico',
# 
#     # Extras (as per Nisbett & Cohen)
#     'missouri', 'nevada',
# }
# NORTH = {
#     'california',
#     'colorado',
#     'connecticut',
#     'delaware',
#     'idaho',
#     'illinois',
#     'indiana',
#     'iowa',
#     'kansas',
#     'maine',
#     'maryland',
#     'massachusetts',
#     'michigan',
#     'minnesota',
#     'montana',
#     'nebraska',
#     'new_hampshire',
#     'new_jersey',
#     'new_york',
#     'north_dakota',
#     'ohio',
#     'oregon',
#     'pennsylvania',
#     'rhode_island',
#     'south_dakota',
#     'utah',
#     'vermont',
#     'washington',
#     'wisconsin',
#     'wyoming',
# }

# # Experiment 3
# 
# SOUTH = {  # Region 3 (South)
#     # Division 5 (South Atlantic) without DC, MD, and DE (as per Nisbett &
#     # Cohen)
#     'florida', 'georgia', 'north_carolina',
#     'south_carolina', 'virginia', 'west_virginia',
# 
#     # Division 6 (East South Central)
#     'kentucky', 'mississippi', 'tennessee', 'alabama',
# 
#     # Division 7 (West South Central)
#     'arkansas', 'louisiana', 'oklahoma', 'texas',
# 
#     # Southernness-index of 25 or more (as per Nisbett & Cohen)
#     'arizona', 'new_mexico',
# 
#     # Extras (as per Nisbett & Cohen)
#     'missouri', 'nevada', 'kansas', 'colorado', 'maryland',
# }
# NORTH = {
#     'california',
#     'connecticut',
#     'delaware',
#     'idaho',
#     'illinois',
#     'indiana',
#     'iowa',
#     'maine',
#     'massachusetts',
#     'michigan',
#     'minnesota',
#     'montana',
#     'nebraska',
#     'new_hampshire',
#     'new_jersey',
#     'new_york',
#     'north_dakota',
#     'ohio',
#     'oregon',
#     'pennsylvania',
#     'rhode_island',
#     'south_dakota',
#     'utah',
#     'vermont',
#     'washington',
#     'wisconsin',
#     'wyoming',
# }

assert not SOUTH & NORTH and SOUTH | NORTH <= US_STATES


def parse_args():
    parser = ArgumentParser(
        prog='us-states',
        description='Encode US state memberships',
        epilog=f'Copyright (c) {datetime.now().year} - Juho Kim',
    )

    parser.add_argument('input', help='input speakers', type=str)
    parser.add_argument('output', help='Output speakers', type=str)
    parser.add_argument('statistics', help='Statistics', type=str)

    return parser.parse_args()


def main():
    args = parse_args()
    status = True
    statistics = Counter()

    with open(args.input) as file:
        speakers = list(file)

    for i, speaker in enumerate(speakers):
        speakers[i] = {'id': speaker, 'us_states': {'total': 0}}

    while status:
        try:
            line = input()
        except EOFError:
            status = False
        else:
            us_state, us_state_input = line.split()

            with open(us_state_input) as file:
                us_state_speakers = set(file)

            for speaker in tqdm(speakers, desc=us_state):
                if speaker['id'] in us_state_speakers:
                    speaker['us_states'][us_state] = True
                    speaker['us_states']['total'] += 1
                    statistics[us_state] += 1
                else:
                    speaker['us_states'][us_state] = False

    for speaker in speakers:
        us_states = set()

        for us_state in US_STATES:
            speaker['us_states'][f'{us_state}_only'] = False

            if speaker['us_states'][us_state]:
                us_states.add(us_state)

        if len(us_states) == 1:
            us_state = us_states.pop()
            speaker['us_states'][f'{us_state}_only'] = True
            statistics[f'{us_state}_only'] += 1

        del us_states

        south = 0
        north = 0

        for us_state in US_STATES:
            if speaker['us_states'][us_state]:
                if us_state in SOUTH:
                    south += 1
                elif us_state in NORTH:
                    north += 1

        south_single = south == 1 and not north
        north_single = not south and north == 1
        souther = south > north
        norther = south < north
        equal = south == north
        south = south > 0
        north = north > 0
        both = south and north
        south_only = south and not north
        north_only = not south and north
        speaker['us_states']['south_single'] = south_single
        speaker['us_states']['north_single'] = north_single
        speaker['us_states']['souther'] = souther
        speaker['us_states']['norther'] = norther
        speaker['us_states']['equal'] = equal
        speaker['us_states']['south'] = south
        speaker['us_states']['north'] = north
        speaker['us_states']['both'] = both
        speaker['us_states']['south_only'] = south_only
        speaker['us_states']['north_only'] = north_only
        statistics['south_single'] += south_single
        statistics['north_single'] += north_single
        statistics['souther'] += souther
        statistics['norther'] += norther
        statistics['equal'] += equal
        statistics['south'] += south
        statistics['north'] += north
        statistics['both'] += both
        statistics['south_only'] += south_only
        statistics['north_only'] += north_only
        statistics[speaker['us_states']['total']] += 1

    with open(args.output, 'w') as file:
        file.write_all(speakers)

    with open(args.statistics, 'w') as file:
        file.write(statistics)


if __name__ == '__main__':
    main()
