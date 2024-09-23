from argparse import ArgumentParser
from collections import defaultdict
from datetime import datetime
from functools import partial
from itertools import filterfalse
from math import isnan
from statistics import fmean

from jsonlines import open
from tqdm import tqdm


def parse_args():
    parser = ArgumentParser(
        prog='aggregate',
        description='Aggregate calculated metrics for each user.',
        epilog=f'Copyright (c) {datetime.now().year} - Juho Kim',
    )

    parser.add_argument(
        'metrics',
        help='File of speakers (with metrics)',
        type=str,
    )
    parser.add_argument(
        'aggregates',
        help='File of aggregated data',
        type=str,
    )

    return parser.parse_args()


def safemean(values):
    values = list(filterfalse(isnan, values))

    return {'rate': fmean(values), 'count': len(values)}


def main():
    args = parse_args()

    aggregates = defaultdict(list)
    aggregates['us_states'] = defaultdict(partial(defaultdict, list))

    with open(args.metrics) as file:
        speakers = list(file)

    for speaker in tqdm(speakers):
        sub_aggregates = [aggregates]

        for us_state, status in speaker['us_states'].items():
            if isinstance(status, bool) and status:
                sub_aggregates.append(aggregates['us_states'][us_state])

        rates = speaker['metrics']['rates']
        aggression = rates['aggression']
        response = rates['response']
        retaliation = rates['retaliation']

        for sub_aggregate in sub_aggregates:
            sub_aggregate['aggression'].append(aggression)
            sub_aggregate['response'].append(response)
            sub_aggregate['retaliation'].append(retaliation)

    sub_aggregates = [aggregates, *aggregates['us_states'].values()]

    for sub_aggregate in sub_aggregates:
        sub_aggregate['aggression'] = safemean(sub_aggregate['aggression'])
        sub_aggregate['response'] = safemean(sub_aggregate['response'])
        sub_aggregate['retaliation'] = safemean(sub_aggregate['retaliation'])

    with open(args.aggregates, 'w') as file:
        file.write(aggregates)


if __name__ == '__main__':
    main()
