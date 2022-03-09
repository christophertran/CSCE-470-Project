import os
import glob
import csv
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def plot(_data, _bins, _range=(-1, -1)):
    if _range == (-1, -1):
        plt.hist(_data, _bins)
    else:
        plt.hist(_data, _bins, range=_range)

    plt.show()


cols = ["ARTIST_NAME", "ARTIST_URL", "SONG_NAME", "SONG_URL", "LYRICS"]


def fix_data():
    path = "./data/azlyrics-csv/"

    data = {c: [] for c in cols}

    for filename in glob.glob(os.path.join(path, "*.csv")):
        with open(os.path.join(os.getcwd(), filename), "r") as f:
            for row in csv.reader(f):
                if row == cols:
                    continue
                else:
                    data[cols[0]].append(row[0])  # ARTIST_NAME
                    data[cols[1]].append(row[1])  # ARTIST_URL
                    data[cols[2]].append(row[2])  # SONG_NAME
                    data[cols[3]].append(row[3])  # SONG_URL
                    data[cols[4]].append(" ".join(row[4:]))  # LYRICS

    df = pd.DataFrame(data)
    df.to_csv(os.path.join(os.getcwd(), path, "all_data.csv"), index=False)

    print(df.head())
    print(len(df))


def get_lyrics_lengths():
    path = "./data/azlyrics-csv/"

    df = pd.read_csv(os.path.join(os.getcwd(), path, "all_data.csv"))

    all_lengths = []
    for index, row in df.iterrows():
        lyrics = row[cols[4]].split(" ")
        all_lengths.append(len(lyrics))

    return all_lengths


def remove_outliers(_data):
    # Sort the data & find first and third quartile
    q1, q3 = np.percentile(sorted(_data), [25, 75])

    # Find interquartile range (IQR)
    iqr = q3 - q1

    # Find lower bound and upper bound
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)

    # Create new dataset without outliers
    return [l for l in _data if lower_bound <= l <= upper_bound]


def __main__():
    # Fix the data and create a new .csv called all_data.csv
    # This all_data.csv can't be committed because it is too large!!!!
    fix_data()

    # Return a list will all the lengths of the lyrics
    all_lengths = np.array(get_lyrics_lengths())

    print("Inluding outliers: ")
    print("Min: ", np.min(all_lengths))
    print("Max: ", np.max(all_lengths))
    print("Avg: ", np.sum(all_lengths) // all_lengths.size)
    print(len(all_lengths))

    # Remove outliers from initial list by calculating IQR
    all_lengths2 = np.array(remove_outliers(all_lengths))

    print("Excluding outliers: ")
    print("Min: ", np.min(all_lengths2))
    print("Max: ", np.max(all_lengths2))
    print("Avg: ", np.sum(all_lengths2) // all_lengths2.size)
    print(len(all_lengths2))

    plot(all_lengths2, 500)


__main__()
