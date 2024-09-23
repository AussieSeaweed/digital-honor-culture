from argparse import ArgumentParser
from convokit import Corpus, download
from datetime import datetime

from jsonlines import open


def parse_args():
    parser = ArgumentParser(
        prog='speakers',
        description='Extract speakers from a ConvoKit corpus',
        epilog=f'Copyright (c) {datetime.now().year} - Juho Kim',
    )

    parser.add_argument('corpus', help='ConvoKit corpus to be used', type=str)
    parser.add_argument('speakers', help='Output file of speakers', type=str)

    return parser.parse_args()


def main():
    args = parse_args()
    corpus = Corpus(download(args.corpus, False))

    corpus.print_summary_stats()

    speakers = []

    for speaker in corpus.speakers.values():
        speakers.append(speaker.id)

    with open(args.speakers, 'w') as file:
        file.write_all(speakers)


if __name__ == '__main__':
    main()
