from argparse import ArgumentParser
from datetime import datetime
from itertools import starmap
from operator import itemgetter

from jsonlines import open
from tqdm import tqdm

SYSTEM_PROMPT = '''
Your response should only be either "YES" or "NO" (without quotes).
'''.strip()
USER_PROMPT = '''
Is this social media post a personal attack?

Post: {}
'''.strip()
YES = 'YES'
NO = 'NO'


def parse_args():
    parser = ArgumentParser(
        prog='fine-tune',
        description=(
            'Generate dataset for classifying utterances as personal attacks'
            ' (or not)'
        ),
        epilog=f'Copyright (c) {datetime.now().year} - Juho Kim',
    )

    parser.add_argument('input', help='Input file of utterances', type=str)
    parser.add_argument('output', help='Output file of dataset', type=str)

    return parser.parse_args()


def create_row(text, status):
    row = {
        'messages': [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': USER_PROMPT.format(text)},
            {'role': 'assistant', 'content': YES if status else NO},
        ],
    }

    return row


def main():
    args = parse_args()

    with open(args.input) as file:
        utterances = list(file)

    dataset = tuple(
        tqdm(
            starmap(
                create_row,
                zip(
                    map(itemgetter('text'), utterances),
                    map(itemgetter('comment_has_personal_attack'), utterances),
                ),
            ),
            total=len(utterances),
        ),
    )

    with open(args.output, 'w') as file:
        file.write_all(dataset)


if __name__ == '__main__':
    main()
