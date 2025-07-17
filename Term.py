class Term:
    def __init__(self, word, lemma, synset):
        self.word = word
        self.lemma = lemma
        self.synset = synset

    def __repr__(self):
        return f"Term(word={self.word}, lemma={self.lemma}, synset={self.synset})"
