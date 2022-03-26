class BM25:
    def __init__(self, corpus):
        print("len(corpus): " + str(len(corpus)))

    def _calculate_avg_lengths():
        """
        TODO: Your code here
        Initialize any data structures needed, perform
        any preprocessing you would like to do on the fields,
        accumulate lengths of fields.
        handle pagerank.
        """

        """
        TODO: Your code here
        Normalize lengths to get average lengths for
        each field (body, title).
        """
        pass

    def _get_net_score():
        """
        TODO: Your code here
        Use equation 3 first and then equation 4 in the writeup to compute the
        overall score
        of a document d for a query q.
        """
        pass

    def _normalize_tfs():
        """
        TODO: Your code here
        Use equation 2 in the writeup to normalize the raw term frequencies
        in fields in document d.
        """
        pass
