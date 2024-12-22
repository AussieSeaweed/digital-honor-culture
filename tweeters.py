from argparse import ArgumentParser
from datetime import datetime
from os import getenv
from re import fullmatch
from sys import setrecursionlimit
from traceback import print_exc

from dotenv import load_dotenv
from jsonlines import open
from tqdm import tqdm
from tweepy import Client

MAX_RESULTS = 100
USER_FIELDS = [
    'created_at',
    'description',
    'entities',
    'id',
    'location',
    'name',
    'pinned_tweet_id',
    'profile_image_url',
    'protected',
    'public_metrics',
    'url',
    'username',
    'verified',
    'withheld',
]
EXPANSIONS = ['pinned_tweet_id']


def parse_args():
    parser = ArgumentParser(
        prog='tweeters',
        description='Get Twitter information.',
        epilog=f'Copyright (c) {datetime.now().year} - Juho Kim',
    )

    parser.add_argument('speakers', help='File of speakers', type=str)
    parser.add_argument(
        'tweeters',
        help='File of speakers (with Twitter information)',
        type=str,
    )

    return parser.parse_args()


def main():
    setrecursionlimit(1000000)
    load_dotenv()

    args = parse_args()
    client = Client(getenv('X_BEARER_TOKEN'))

    try:
        with open(args.tweeters) as file:
            speakers = list(file)
    except FileNotFoundError:
        with open(args.speakers) as file:
            speakers = list(file)

    indices = []
    usernames = []

    for i, speaker in enumerate(speakers):
        if 'tweeter' in speaker:
            continue

        if fullmatch(r'^[A-Za-z0-9_]{1,15}$', speaker['id']):
            indices.append(i)
            usernames.append(speaker['id'])
        else:
            speaker['tweeter'] = None

    users = []

    for i in tqdm(range(0, len(usernames), MAX_RESULTS)):
        try:
            response = client.get_users(
                usernames=usernames[i:i + MAX_RESULTS],
                user_fields=USER_FIELDS,
                expansions=EXPANSIONS,
            )
        except:  # noqa: E722
            print_exc()

            break

        sub_users = {user.username: user for user in response[0]}

        for username in usernames[i:i + MAX_RESULTS]:
            if username in sub_users:
                user = sub_users[username]
                user = {
                    key: getattr(user, key) for key in USER_FIELDS + EXPANSIONS
                }

                for key in user.keys():
                    if isinstance(user[key], datetime):
                        user[key] = user[key].isoformat()

                users.append(user)
            else:
                users.append(None)

    for i, user in zip(indices, users):
        speakers[i]['tweeter'] = user

    with open(args.tweeters, 'w') as file:
        file.write_all(speakers)


if __name__ == '__main__':
    main()
