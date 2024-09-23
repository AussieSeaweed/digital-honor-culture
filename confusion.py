from argparse import ArgumentParser
from datetime import datetime

from jsonlines import open


def parse_args():
    parser = ArgumentParser(
        prog='confusion',
        description='Evaluate predicted classifications',
        epilog=f'Copyright (c) {datetime.now().year} - Juho Kim',
    )

    parser.add_argument(
        'actual',
        help='Actual classifications of utterances',
        type=str,
    )
    parser.add_argument(
        'predicted',
        help='Predicted classifications of utterances',
        type=str,
    )
    parser.add_argument('output', help='Output confusion values', type=str)

    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.actual) as file:
        actual_classifications = list(file)

    with open(args.predicted) as file:
        predicted_classifications = list(file)

    confusion = {
        'total': 0,
        'actual_positive': 0,
        'actual_negative': 0,
        'predicted_positive': 0,
        'predicted_negative': 0,
        'true_positive': 0,
        'false_positive': 0,
        'true_negative': 0,
        'false_negative': 0,
    }

    for actual, predicted in zip(
            actual_classifications,
            predicted_classifications,
    ):
        confusion['total'] += 1
        confusion['actual_positive'] += actual['comment_has_personal_attack']
        confusion['actual_negative'] += (
            not actual['comment_has_personal_attack']
        )
        confusion['predicted_positive'] += (
            predicted['comment_has_personal_attack']
        )
        confusion['predicted_negative'] += (
            not predicted['comment_has_personal_attack']
        )
        confusion['true_positive'] += (
            actual['comment_has_personal_attack']
            and predicted['comment_has_personal_attack']
        )
        confusion['false_positive'] += (
            not actual['comment_has_personal_attack']
            and predicted['comment_has_personal_attack']
        )
        confusion['false_negative'] += (
            actual['comment_has_personal_attack']
            and not predicted['comment_has_personal_attack']
        )
        confusion['true_negative'] += (
            not actual['comment_has_personal_attack']
            and not predicted['comment_has_personal_attack']
        )

    with open(args.output, 'w') as file:
        file.write(confusion)


if __name__ == '__main__':
    main()
