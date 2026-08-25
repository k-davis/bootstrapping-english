from Synset import Synset
from nltk.corpus import wordnet as wn

class Conjugation:
    def __init__(self, conjugation: str):
        self.conjugation: str = conjugation
        
    def possible_synsets(self) -> list[Synset]:
        synsets = wn.synsets(self.conjugation)
        return [Synset.from_wn_synset(synset.name()) for synset in synsets] # type: ignore
    
    def __str__(self) -> str:
        return self.conjugation