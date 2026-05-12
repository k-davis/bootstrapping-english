
class Lemma:
    def __init__(self):
        # The word and lemma can differ
        #  As in word Salt, but lemmas Salt, Saltiness, and Salinity
        self.word: str = ""
        self.lemma: str = ""
        self.pos: str = ""
        # self.definition... Lemmas do not have definitions in WordNet

    def __str__(self) -> str:
        return "Lemma(word={}, lemma={}, pos={})".format(self.word, self.lemma, self.pos)

