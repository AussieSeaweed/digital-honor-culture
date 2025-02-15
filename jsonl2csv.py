from sys import stdin, stdout

from jsonlines import Reader
import pandas as pd


def main():
    data = list(Reader(stdin))
    df = pd.json_normalize(data).dropna(axis=1, how='all')

    df.to_csv(stdout)


if __name__ == '__main__':
    main()
