from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import partial
from operator import itemgetter
from warnings import warn

from dotenv import load_dotenv
from jsonlines import open
from openai import OpenAI
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
        prog='classify',
        description='Classify utterances as personal attacks (or not)',
        epilog=f'Copyright (c) {datetime.now().year} - Juho Kim',
    )

    parser.add_argument('input', help='Input file of utterances', type=str)
    parser.add_argument('output', help='Output file of utterances', type=str)
    parser.add_argument('model', help='OpenAI chat model', type=str)
    parser.add_argument('max_workers', help='max number of workers', type=int)

    return parser.parse_args()


def classify(client, model, text):
    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': USER_PROMPT.format(text)},
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

    if response == YES:
        classification = True
    elif response == NO:
        classification = False
    else:
        classification = False

        warn(f'Cannot get verdict for {messages}')

    return classification


def main():
    load_dotenv()

    args = parse_args()
    client = OpenAI()

    with open(args.input) as file:
        utterances = list(file)

    with ThreadPoolExecutor(args.max_workers) as executor:
        classifications = tuple(
            tqdm(
                executor.map(
                    partial(classify, client, args.model),
                    map(itemgetter('text'), utterances),
                ),
                total=len(utterances),
            ),
        )

    for utterance, classification in zip(utterances, classifications):
        utterance['comment_has_personal_attack'] = classification

    with open(args.output, 'w') as file:
        file.write_all(utterances)


if __name__ == '__main__':
    main()
