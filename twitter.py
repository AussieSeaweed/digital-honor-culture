from argparse import ArgumentParser
from datetime import datetime

from jsonlines import open
from tqdm import tqdm
import pandas as pd


def parse_args():
    parser = ArgumentParser(
        prog='twitter',
        description='Twtiter annotated locations for each user.',
        epilog=f'Copyright (c) {datetime.now().year} - Juho Kim',
    )

    parser.add_argument(
        'speakers',
        help='File of speakers (with metrics)',
        type=str,
    )
    parser.add_argument(
        'twitter',
        help='File of twitter-annotated data',
        type=str,
    )
    parser.add_argument(
        'output',
        help='File of output data',
        type=str,
    )

    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.speakers) as file:
        speakers = list(file)

    df = pd.read_csv(
        args.twitter,
        index_col=0,
        dtype={'id': str, 'location': str, 'us_region': str},
        na_filter=False,
    )
    locations = {row['id']: row['location'] for _, row in df.iterrows()}
    us_regions = {row['id']: row['us_region'] for _, row in df.iterrows()}

    for speaker in tqdm(speakers):
        speaker_id = speaker['id']
        us_states = tuple(speaker['us_states'].keys())
        location = locations[speaker_id]
        us_region = us_regions[speaker_id]

        for us_state in us_states:
            speaker['us_states'][f'{us_state}_with_twitter_location'] = (
                speaker['us_states'][us_state]
                and bool(location)
            )

        for us_state in us_states:
            speaker['us_states'][f'{us_state}_with_twitter_us_region'] = (
                speaker['us_states'][us_state]
                and bool(us_region)
            )

        match us_region:
            case 'SOUTH':
                speaker['us_states']['south_twitter'] = True
                speaker['us_states']['north_twitter'] = False
            case 'NON-SOUTH':
                speaker['us_states']['south_twitter'] = False
                speaker['us_states']['north_twitter'] = True
            case '':
                speaker['us_states']['south_twitter'] = False
                speaker['us_states']['north_twitter'] = False
            case _:
                raise AssertionError

    with open(args.output, 'w') as file:
        file.write_all(speakers)


if __name__ == '__main__':
    main()
