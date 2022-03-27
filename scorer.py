import re
import math

from collections import Counter


class Query:
    def __init__(self, _query):
        self.query = _query
        self.query_words = re.sub(r"[^a-zA-Z0-9_ ]", "", _query).split(" ")
        self.query_words = [query_word.lower() for query_word in self.query_words]


class BM25:
    def __init__(self, _corpus, _k1=1.5, _b=0.75, _epsilon=0.25):
        print("len(corpus): " + str(len(_corpus)))
        self.corpus = _corpus
        self.df = (
            {}
        )  # df, doc frequency aka number of docs containing the term; word -> # of docs with word
        self.tf = (
            []
        )  # tf, num of times term t occurs in document d; tf list of dictionaries; dict(term -> freq)
        self.dl = 0  # L_d, length of document (in terms)
        self.avg_dl = 0  # L_avg, mean of the document lengths
        self.n_docs = 0  # N, number of documents
        self.k1 = _k1  # k1, Tuning parameter
        self.b = _b  # b, Tuning parameter
        self.epsilon = _epsilon  # epsilon, Tuning parameter
        self._initialize()

    def _initialize(self):
        for doc in self.corpus:
            self.n_docs += 1  # Calculate N
            self.dl += len(doc)  # Calculate L_d

            # Calculate tf (term frequencies) of the current doc
            self.tf.append(Counter(doc))

            # Update df
            for word in doc:
                self.df[word] = self.df.get(word, 0) + 1

        # Calc L_avg
        self.avg_dl = self.dl / self.n_docs

    def _calc_idfs(self, _query):
        idfs = []

        for term in _query.query_words:
            # TODO: This could be a problem if term doesn't exist in documents.
            # Because we would have a divide by zero error. Need to fix this.
            if term not in self.df:
                idfs.append(0)
                continue

            idfs.append(math.log10(self.n_docs / self.df[term]))

        # TODO: The epsilon value is something I found online, not 100% sure
        # what it actually is and means.
        eps = (sum(idfs) / len(idfs)) * self.epsilon

        for i, idf in enumerate(idfs):
            if idf < 0:
                idfs[i] = eps

        return idfs

    # Calculates the rsv, or retrieval status value, for a given query. They are the sums
    # of individual term (t) scores for each song (doc).
    def _get_rsvs(self, _query):
        rsvs = []

        idfs = self._calc_idfs(_query)
        for i in range(len(self.tf)):
            rsv = 0

            for j, term in enumerate(_query.query_words):
                idf = idfs[j]
                right_side = ((self.k1 + 1) * self.tf[i][term]) / (
                    self.k1 * (1 - self.b + (self.b * (self.dl / self.avg_dl)))
                    + self.tf[i][term]
                )

                rsv += idf * right_side

            rsvs.append(rsv)

        return rsvs

    def get_top_n(self, _query, _n=5):
        rsvs = self._get_rsvs(_query)
        rsvs = [(i, rsv) for i, rsv in enumerate(rsvs)]

        rsvs.sort(key=lambda x: x[1], reverse=True)

        return [rsv[0] for rsv in rsvs[:_n]]
