"""

This script...

1. Creates all_data.csv
2. Upload the csv to a mongodb cluster

This script should be ran before deploying the web app (if it hasn't been ran before)
since this script will create the db that the web app will use.

"""

import os
import re
import csv
import glob
import json

import pymongo
import pandas as pd

from scripts.stopwords import STOPWORDS

NROWS = None
COLS = ["ARTIST_NAME", "ARTIST_URL", "SONG_NAME", "SONG_URL", "LYRICS"]

username = "testuser"
password = "0M6YRahVFlTKMad5"
database_name = "csce470"
collection_name = "songs"

path = os.path.join(os.getcwd(), "data", "azlyrics-csv")
filename = "all_data.csv"

all_data_path = os.path.join(path, filename)


def create_all_data(_path, _filename):
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


def mongoImport(csv_path):
    client = pymongo.MongoClient(
        f"mongodb+srv://{username}:{password}@cluster0.wqbto.mongodb.net"
    )

    db = client[database_name]
    coll = db[collection_name]

    data = pd.read_csv(csv_path, nrows=NROWS)

    # Remove non alphanumeric characters
    data[COLS[4]] = data[COLS[4]].apply(
        lambda lyrics: (" ").join(re.sub(r"[^a-zA-Z0-9_ ]", "", lyrics).split(" "))
    )

    def removeStopwords(lyrics):
        return " ".join(
            [
                lyric.lower()
                for lyric in lyrics.split(" ")
                if lyric.lower() not in STOPWORDS
            ]
        )

    # Remove stopwords
    data[COLS[4]] = data[COLS[4]].apply(removeStopwords)

    payload = json.loads(data.to_json(orient="records"))

    coll.drop()
    coll.insert_many(payload)

    return coll.count_documents({})


print("Created all_data.csv? ", create_all_data(path, filename))
print("# of docs inserted in db: ", mongoImport(csv_path=all_data_path))
