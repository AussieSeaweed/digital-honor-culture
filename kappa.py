from argparse import ArgumentParser
from datetime import datetime
from pprint import pformat

from jsonlines import open
from sklearn.metrics import cohen_kappa_score

SOUTH = 'SOUTH'
NORTH = 'NORTH'


def parse_args():
    parser = ArgumentParser(
        prog='Kappa',
        description='Kappa measure for US region classifications',
        epilog=f'Copyright (c) {datetime.now().year} - Juho Kim',
    )

    parser.add_argument('speakers', help='File of speakers', type=str)

    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.speakers) as file:
        speakers = list(file)

    regions1 = []
    regions2 = []

    for speaker in speakers:
        region1 = speaker['region']
        region2 = speaker['region2']

        if region1 not in {SOUTH, NORTH} or region2 not in {SOUTH, NORTH}:
            continue

        regions1.append(region1)
        regions2.append(region2)

    output = {
        'cohen_kappa_score': cohen_kappa_score(regions1, regions2).item(),
        'count': len(regions1),
    }

    print(pformat(output).replace('\'', '"').replace(': nan}', ': null}'))


if __name__ == '__main__':
    main()
