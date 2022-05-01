import time

import pymongo

from scripts.scorer import BM25, Query

# Set CORPUS_LENGTH to None to use ALL docs in the db
# otherwise, set it to however many you want read from the db
CORPUS_LENGTH = 35000


class QueryTool:
    def __init__(self):
        self.username = "testuser"
        self.password = "0M6YRahVFlTKMad5"
        self.database_name = "csce470"
        self.collection_name = "songs"

        self.client = pymongo.MongoClient(
            f"mongodb+srv://{self.username}:{self.password}@cluster0.wqbto.mongodb.net"
        )

        self.database = self.client[self.database_name]
        self.collection = self.database[self.collection_name]

        self.doc_ids = []
        self.scorer = None

        self._setup()

    def _setup(self):
        print("-" * 25)
        print("STARTING SETUP OF BM25 SCORER")
        start_time = time.time()

        # Create corpus with lyrics in database
        # Create id list to query database for song info
        corpus = []
        count = 0
        for doc in self.collection.find({}, {"LYRICS": 1}):
            self.doc_ids.append(doc["_id"])

            # Tokenize the lyrics of the song
            corpus.append(doc["LYRICS"].split(" "))

            count += 1
            if CORPUS_LENGTH and count >= CORPUS_LENGTH:
                break

        self.scorer = BM25()
        self.scorer.fit(corpus)

        print("Corpus Length: ", len(corpus))
        print(f"Setup time: {time.time() - start_time} seconds")
        print("ENDING SETUP OF BM25 SCORER")
        print("-" * 25)

    def query(self, _query, _n=5):
        if not _query:
            return []

        indexes = self.scorer.query_n(Query(_query), _n)

        if not indexes:
            return []

        return [
            self.collection.find({"_id": self.doc_ids[index]})[0] for index in indexes
        ]
