from argparse import ArgumentParser
from datetime import datetime
from os import getenv
from time import sleep

from dotenv import load_dotenv
from jsonlines import open
from prawcore.exceptions import NotFound
from praw import Reddit
from tqdm import tqdm


def parse_args():
    parser = ArgumentParser(
        prog='redditors',
        description='Get redditor information.',
        epilog=f'Copyright (c) {datetime.now().year} - Juho Kim',
    )

    parser.add_argument('speakers', help='File of speakers', type=str)
    parser.add_argument(
        'redditors',
        help='File of speakers (with redditor information)',
        type=str,
    )

    return parser.parse_args()


def main():
    load_dotenv()

    args = parse_args()
    reddit = Reddit(
        client_id=getenv('REDDIT_CLIENT_ID'),
        client_secret=getenv('REDDIT_CLIENT_SECRET'),
        user_agent=getenv('REDDIT_USER_AGENT'),
        ratelimit_seconds=600,
    )

    with open(args.speakers) as file:
        speakers = list(file)

    redditors = {}

    try:
        with open(args.redditors) as file:
            for redditor in file:
                redditors[redditor['id']] = redditor['redditor']
    except FileNotFoundError:
        pass

    with open(args.redditors, 'w') as file:
        for speaker in tqdm(speakers):
            if speaker['id'] in redditors:
                speaker['redditor'] = redditors[speaker['id']]
            else:
                try:
                    redditor = reddit.redditor(speaker['id'])
                    speaker['redditor'] = {
                        'comment_karma': getattr(
                            redditor,
                            'comment_karma',
                            None,
                        ),
                        'created_utc': getattr(redditor, 'created_utc', None),
                        'has_verified_email': getattr(
                            redditor,
                            'has_verified_email',
                            None,
                        ),
                        'icon_img': getattr(redditor, 'icon_img', None),
                        'id': getattr(redditor, 'id', None),
                        'is_employee': getattr(redditor, 'is_employee', None),
                        'is_mod': getattr(redditor, 'is_mod', None),
                        'is_gold': getattr(redditor, 'is_gold', None),
                        'is_suspended': getattr(
                            redditor,
                            'is_suspended',
                            None,
                        ),
                        'link_karma': getattr(redditor, 'link_karma', None),
                    }
                except NotFound:
                    speaker['redditor'] = None

                sleep(0.01)

            file.write(speaker)


if __name__ == '__main__':
    main()
