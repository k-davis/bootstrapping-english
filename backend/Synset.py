from typing import Any, Dict
from nltk.corpus import wordnet as wn 

class Synset:
    def __init__(self, name: str, definition: str, pos: str):
        self.name: str = name
        self.definition: str = definition
        self.pos: str = pos

    @classmethod
    def from_wn_synset(cls, synset_name: str):
        synset = wn.synset(synset_name)
        return cls(synset.name(), synset.definition(), synset.pos())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "definition": self.definition,
            "pos": self.pos
        }