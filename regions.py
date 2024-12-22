from argparse import ArgumentParser
from datetime import datetime
from functools import partial
from operator import getitem

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

SOUTHERN_STATES = {  # Region 3 (South)
    # Division 5 (South Atlantic) without DC (as per Nisbett & Cohen)
    'delaware', 'florida', 'georgia', 'maryland', 'north_carolina',
    'south_carolina', 'virginia', 'west_virginia',

    # Division 6 (East South Central)
    'kentucky', 'mississippi', 'tennessee', 'alabama',

    # Division 7 (West South Central)
    'arkansas', 'louisiana', 'oklahoma', 'texas',
}
NORTHERN_STATES = {
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
# SOUTHERN_STATES = {  # Region 3 (South)
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
# NORTHERN_STATES = {
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
# SOUTHERN_STATES = {  # Region 3 (South)
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
# NORTHERN_STATES = {
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

assert (
    not SOUTHERN_STATES & NORTHERN_STATES
    and SOUTHERN_STATES | NORTHERN_STATES <= US_STATES
)


def parse_args():
    parser = ArgumentParser(
        prog='regions',
        description='Assign a US region for each user.',
        epilog=f'Copyright (c) {datetime.now().year} - Juho Kim',
    )

    parser.add_argument('speakers', help='File of speakers', type=str)
    parser.add_argument(
        'regions',
        help='File of speakers (with regions)',
        type=str,
    )

    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.speakers) as file:
        speakers = list(file)

    for speaker in tqdm(speakers):
        us_state_count = sum(
            map(partial(getitem, speaker['speakerships']), US_STATES),
        )
        south_count = sum(
            map(partial(getitem, speaker['speakerships']), SOUTHERN_STATES),
        )
        north_count = sum(
            map(partial(getitem, speaker['speakerships']), NORTHERN_STATES),
        )

        if us_state_count == 1 and south_count == 1 and not north_count:
            region = 'SOUTH'
        elif us_state_count == 1 and not south_count and north_count == 1:
            region = 'NORTH'
        else:
            region = None

        speaker['region'] = region

    with open(args.regions, 'w') as file:
        file.write_all(speakers)


if __name__ == '__main__':
    main()
