import os
import re
import csv
import glob

import pandas as pd

from rank import BM25

NROWS = 50
COLS = ["ARTIST_NAME", "ARTIST_URL", "SONG_NAME", "SONG_URL", "LYRICS"]


def create_all_data(_path):
    if os.path.exists(_path):
        # If file "_path" already exists, return False
        return False

    data = {c: [] for c in COLS}

    for filename in glob.glob(os.path.join(_path, "*.csv")):
        with open(os.path.join(os.getcwd(), filename), "r") as f:
            for row in csv.reader(f):
                if row == COLS:
                    # Skip the header of the .csv file
                    continue
                else:
                    data[COLS[0]].append(row[0])  # ARTIST_NAME
                    data[COLS[1]].append(row[1])  # ARTIST_URL
                    data[COLS[2]].append(row[2])  # SONG_NAME
                    data[COLS[3]].append(row[3])  # SONG_URL
                    data[COLS[4]].append(" ".join(row[4:]))  # LYRICS

    df = pd.DataFrame(data)
    df.to_csv(_path, index=False)

    # If file "_path" was created, return True
    return True


def read_all_data(_path, _nrows=None):
    if not os.path.exists(_path):
        create_all_data()

    df = pd.read_csv(os.path.join(_path), nrows=_nrows)

    return df


def __main__():
    # Path to location of all_data.csv file
    path = os.path.join(os.getcwd(), "data", "azlyrics-csv", "all_data.csv")

    # Read all data into a pandas dataframe
    all_data_df = read_all_data(path, NROWS)

    # Create corpus with lyrics, tokenize lyrics before adding to corpus.
    corpus = [
        re.sub(r"[^a-zA-Z0-9_ ]", "", row.LYRICS).split(" ")
        for row in all_data_df.itertuples()
    ]

    bm25 = BM25(corpus)


if __name__ == "__main__":
    __main__()
