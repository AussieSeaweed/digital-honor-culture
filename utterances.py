from argparse import ArgumentParser
from convokit import Corpus, download
from datetime import datetime

from jsonlines import open


def parse_args():
    parser = ArgumentParser(
        prog='utterances',
        description='Extract speakers from a ConvoKit corpus',
        epilog=f'Copyright (c) {datetime.now().year} - Juho Kim',
    )

    parser.add_argument('corpus', help='ConvoKit corpus to be used', type=str)
    parser.add_argument(
        'utterances',
        help='Output file of utterances',
        type=str,
    )

    return parser.parse_args()


def main():
    args = parse_args()
    corpus = Corpus(download(args.corpus, False))

    corpus.print_summary_stats()

    utterances = []

    for utterance in corpus.utterances.values():
        utterances.append(
            {
                'id': utterance.id,
                'reply_to': utterance.reply_to,
                'speaker_id': utterance.speaker.id,
                'text': utterance.text,
                'comment_has_personal_attack': utterance.meta.get(
                    'comment_has_personal_attack',
                ),
            },
        )

    with open(args.utterances, 'w') as file:
        file.write_all(utterances)


if __name__ == '__main__':
    main()
