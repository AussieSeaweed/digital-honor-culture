from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import partial
from warnings import warn

from dotenv import load_dotenv
from jsonlines import open
from openai import OpenAI
from tqdm import tqdm

SYSTEM_PROMPT = (
    'Your response should only be one of "NORTH", "SOUTH", or "N/A" (without'
    ' quotes).'
)
USER_PROMPT = '''
What US region is the following location in?

Location: {}
'''.strip()
NORTH = 'NORTH'
SOUTH = 'SOUTH'
NOT_APPLICABLE = 'N/A'


def parse_args():
    parser = ArgumentParser(
        prog='regions2',
        description='Classify US regions from Twitter locations.',
        epilog=f'Copyright (c) {datetime.now().year} - Juho Kim',
    )

    parser.add_argument('speakers', help='File of speakers', type=str)
    parser.add_argument(
        'regions',
        help='File of speakers (with regions)',
        type=str,
    )
    parser.add_argument('model', help='OpenAI chat model', type=str)
    parser.add_argument('max_workers', help='max number of workers', type=int)

    return parser.parse_args()


def classify(client, model, location):
    if location is None or not location:
        return None

    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': USER_PROMPT.format(location)},
    ]

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        response = completion.choices[0].message.content
    except Exception as e:  # noqa: E722
        response = None

        warn(f'Exception {repr(e)} occurred while evaluating {messages}')

    messages.append({'role': 'assistant', 'content': response})

    if response == NORTH:
        classification = NORTH
    elif response == SOUTH:
        classification = SOUTH
    elif response == NOT_APPLICABLE:
        classification = None
    else:
        classification = None

        warn(f'Cannot get verdict for {messages}')

    return classification


def main():
    load_dotenv()

    args = parse_args()
    client = OpenAI()

    with open(args.speakers) as file:
        speakers = list(file)

    locations = []

    for speaker in tqdm(speakers):
        if speaker['tweeter'] is not None:
            location = speaker['tweeter']['location']
        else:
            location = None

        locations.append(location)

    with ThreadPoolExecutor(args.max_workers) as executor:
        classifications = tuple(
            tqdm(
                executor.map(partial(classify, client, args.model), locations),
                total=len(locations),
            ),
        )

    for speaker, classification in zip(speakers, classifications):
        speaker['region2'] = classification

    with open(args.regions, 'w') as file:
        file.write_all(speakers)


if __name__ == '__main__':
    main()
