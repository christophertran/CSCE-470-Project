import os
import re
import csv
import glob

import pandas as pd

from scripts.scorer import BM25, Query
from scripts.stopwords import STOPWORDS


# Number of rows to read from all_data.csv, set to "None" to read all data
NROWS = None
COLS = ["ARTIST_NAME", "ARTIST_URL", "SONG_NAME", "SONG_URL", "LYRICS"]


SCORER = None
ALL_DATA_DF = pd.DataFrame()


def create_all_data(_path, _filename):
    global COLS

    if os.path.exists(os.path.join(_path, _filename)):
        os.remove(os.path.join(_path, _filename))

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
    df.to_csv(os.path.join(_path, _filename), index=False)

    # If file "_path" was created, return True
    return True


def read_all_data(_path, _filename, _nrows=None):
    if not os.path.exists(os.path.join(_path, _filename)):
        create_all_data(_path, _filename)

    df = pd.read_csv(os.path.join(_path, _filename), nrows=_nrows)

    return df


def setup():
    print("-" * 25)
    print("STARTING SETUP OF BM25 SCORER")

    global NROWS
    global SCORER
    global ALL_DATA_DF

    # Path to location of all_data.csv file
    path = os.path.join(os.getcwd(), "data", "azlyrics-csv")
    filename = "all_data.csv"

    # Read all data into a pandas dataframe
    ALL_DATA_DF = read_all_data(path, filename, NROWS)

    # Create corpus with lyrics, tokenize lyrics before adding to corpus.
    corpus = [
        re.sub(r"[^a-zA-Z0-9_ ]", "", row.LYRICS).split(" ")
        for row in ALL_DATA_DF.itertuples()
    ]

    corpus = [
        [lyric.lower() for lyric in lyrics if lyric.lower() not in STOPWORDS]
        for lyrics in corpus
    ]

    SCORER = BM25()
    SCORER.fit(corpus)
    print("Corpus Length: ", len(corpus))
    print("ENDING SETUP OF BM25 SCORER")
    print("-" * 25)


def query(_query, _n=5):
    global COLS
    global SCORER
    global ALL_DATA_DF

    if not _query:
        return pd.DataFrame()

    if not SCORER or ALL_DATA_DF.empty:
        setup()

    indexes = SCORER.query_n(Query(_query), _n)

    if indexes:
        return ALL_DATA_DF.loc[indexes].to_string(index=False)
    else:
        return pd.DataFrame()
