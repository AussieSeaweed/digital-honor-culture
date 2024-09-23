from argparse import ArgumentParser
from datetime import datetime
from math import nan

from jsonlines import open
from tqdm import tqdm


def parse_args():
    parser = ArgumentParser(
        prog='metrics',
        description='Calculate metrics for each user.',
        epilog=f'Copyright (c) {datetime.now().year} - Juho Kim',
    )

    parser.add_argument('utterances', help='File of utterances', type=str)
    parser.add_argument('speakers', help='File of speakers', type=str)
    parser.add_argument(
        'metrics',
        help='File of speakers (with metrics)',
        type=str,
    )

    return parser.parse_args()


def safediv(dividend, divisor):
    if divisor:
        quotient = dividend / divisor
    else:
        quotient = nan

    return quotient


def main():
    args = parse_args()

    with open(args.speakers) as file:
        speakers = list(file)

    speaker_lookup = {}

    for speaker in tqdm(speakers):
        speaker['metrics'] = {
            'counts': {
                # AGG
                'personal_attacks': 0,
                # AGG
                'utterances': 0,
                # RESP
                'personally_attacked': 0,
                # RESP & RET
                'responses': 0,
                # RET
                'retaliations': 0,
            },
        }
        speaker_lookup[speaker['id']] = speaker

    with open(args.utterances) as file:
        utterances = list(file)

    assert None not in speaker_lookup

    utterance_lookup = {}

    for utterance in tqdm(utterances):
        speaker = speaker_lookup.get(utterance['speaker_id'])

        if speaker is not None:
            speaker['metrics']['counts']['personal_attacks'] += (
                utterance['comment_has_personal_attack']
            )
            speaker['metrics']['counts']['utterances'] += 1

        utterance_lookup[utterance['id']] = utterance

    assert None not in utterance_lookup

    personal_attack_lookup = {}

    for utterance in tqdm(utterances):
        if not utterance['comment_has_personal_attack']:
            continue

        parent = utterance_lookup.get(utterance['reply_to'])

        if parent is None:
            continue

        speaker = speaker_lookup.get(parent['speaker_id'])

        if speaker is None:
            continue

        speaker['metrics']['counts']['personally_attacked'] += 1
        personal_attack_lookup[utterance['id']] = utterance

    for utterance in tqdm(utterances):
        speaker = speaker_lookup.get(utterance['speaker_id'])

        if speaker is None:
            continue

        parent = personal_attack_lookup.get(utterance['reply_to'])

        if (
                parent is None
                or (
                    speaker['id']
                    != utterance_lookup[parent['reply_to']]['speaker_id']
                )
        ):
            continue

        speaker['metrics']['counts']['responses'] += 1
        speaker['metrics']['counts']['retaliations'] += (
            utterance['comment_has_personal_attack']
        )

    for speaker in tqdm(speakers):
        metrics = speaker['metrics']
        counts = metrics['counts']
        metrics['rates'] = {
            'aggression': safediv(
                counts['personal_attacks'],
                counts['utterances'],
            ),
            'response': safediv(
                counts['responses'],
                counts['personally_attacked'],
            ),
            'retaliation': safediv(
                counts['retaliations'],
                counts['responses'],
            ),
        }

    with open(args.metrics, 'w') as file:
        file.write_all(speakers)


if __name__ == '__main__':
    main()
