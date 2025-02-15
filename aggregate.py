from argparse import ArgumentParser
from datetime import datetime
from itertools import filterfalse
from math import isnan, nan
from pprint import pformat
from statistics import fmean

from jsonlines import open

RATE_KEYS = 'aggression', 'response', 'retaliation'
REGION_KEY = 'region2'


def parse_args():
    parser = ArgumentParser(
        prog='aggregate',
        description='Aggregate calculated metrics for each user.',
        epilog=f'Copyright (c) {datetime.now().year} - Juho Kim',
    )

    parser.add_argument('speakers', help='File of speakers', type=str)

    return parser.parse_args()


def safemean(values):
    values = list(filterfalse(isnan, values))

    return {'rate': (fmean(values) if values else nan), 'count': len(values)}


def rates_of(speakers, key):
    rates = []

    for speaker in speakers:
        rates.append(speaker['metrics']['rates'][key])

    return rates


def aggregate(speakers):
    return {key: safemean(rates_of(speakers, key)) for key in RATE_KEYS}


def separate_by_region(speakers):
    northerners = []
    southerners = []

    for speaker in speakers:
        match speaker[REGION_KEY]:
            case 'NORTH':
                northerners.append(speaker)
            case 'SOUTH':
                southerners.append(speaker)
            case _:
                pass

    return northerners, southerners


def separate_by_bool(speakers, key_function):
    truthies = []
    falsies = []

    for speaker in speakers:
        key = key_function(speaker)

        if key is True:
            truthies.append(speaker)
        elif key is False:
            falsies.append(speaker)

    return truthies, falsies


def bool_of(speakers, key_function):
    truthies, falsies = separate_by_bool(speakers, key_function)
    truthy_northerners, truthy_southerners = separate_by_region(truthies)
    falsy_northerners, falsy_southerners = separate_by_region(falsies)

    return {
        'TRUTHY': {
            'NORTH': aggregate(truthy_northerners),
            'SOUTH': aggregate(truthy_southerners),
        },
        'FALSY': {
            'NORTH': aggregate(falsy_northerners),
            'SOUTH': aggregate(falsy_southerners),
        },
    }


def bool_redditor_of(speakers, key):
    return bool_of(
        speakers,
        lambda speaker: (
            None
            if speaker['redditor'] is None
            else speaker['redditor'][key]
        ),
    )


def main():
    args = parse_args()

    with open(args.speakers) as file:
        speakers = list(file)

    for speaker in speakers:
        if speaker['redditor'] is None:
            continue
        elif speaker['redditor']['icon_img'] is None:
            speaker['redditor']['has_default_icon'] = None
        else:
            assert isinstance(speaker['redditor']['icon_img'], str)

            speaker['redditor']['has_default_icon'] = (
                'default'
                in speaker['redditor']['icon_img']
            )

    aggregates = {}

    for key in (
            'has_verified_email',
            'has_default_icon',
            'is_mod',
            'is_gold',
    ):
        aggregates[key] = bool_redditor_of(speakers, key)

    northerners, southerners = separate_by_region(speakers)
    aggregates[''] = {
        'NORTH': aggregate(northerners),
        'SOUTH': aggregate(southerners),
    }
    aggregates['has_twitter'] = bool_of(
        speakers,
        lambda speaker: speaker['tweeter'] is not None,
    )

    print(pformat(aggregates).replace('\'', '"').replace(': nan}', ': null}'))


if __name__ == '__main__':
    main()
