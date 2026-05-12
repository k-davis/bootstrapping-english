from typing import Any, Dict
from nltk.corpus import wordnet as wn 

class Synset:
    def __init__(self, name: str, definition: str, pos: str):
        self.name: str = name
        self.definition: str = definition
        self.pos: str = pos

    def __str__(self) -> str:
        return "Synset(name={}, pos={}, definition={})".format(self.name, self.pos, self.definition)
    
    @classmethod
    def from_wn_synset(cls, synset_id: str):
        synset = wn.synset(synset_id)
        #lemmas = synset.Lemmas()
        return cls(synset.name(), synset.definition(), synset.pos()) # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            "synset_id": self.name,
            "definition": self.definition,
            "pos": self.pos
        }