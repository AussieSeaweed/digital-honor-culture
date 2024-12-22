from argparse import ArgumentParser
from collections import Counter
from datetime import datetime

from jsonlines import open
from tqdm import tqdm


def parse_args():
    parser = ArgumentParser(
        prog='speakerships',
        description='Encode speakerships',
        epilog=f'Copyright (c) {datetime.now().year} - Juho Kim',
    )

    parser.add_argument('input', help='Input speakers', type=str)
    parser.add_argument('output', help='Output speakers', type=str)
    parser.add_argument('counts', help='Counts', type=str)

    return parser.parse_args()


def main():
    args = parse_args()
    status = True
    counts = Counter()

    with open(args.input) as file:
        speakers = list(file)

    for i, speaker in enumerate(speakers):
        speakers[i] = {'id': speaker, 'speakerships': {}}

    while status:
        try:
            line = input()
        except EOFError:
            status = False
        else:
            speakership, speakership_input = line.split()

            with open(speakership_input) as file:
                speakership_speakers = set(file)

            for speaker in tqdm(speakers, desc=speakership):
                if speaker['id'] in speakership_speakers:
                    speaker['speakerships'][speakership] = True
                    counts[speakership] += 1
                else:
                    speaker['speakerships'][speakership] = False

    with open(args.output, 'w') as file:
        file.write_all(speakers)

    with open(args.counts, 'w') as file:
        file.write(counts)


if __name__ == '__main__':
    main()
