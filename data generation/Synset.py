from typing import Any, Dict
from typing_extensions import Self
from nltk.corpus import wordnet as wn 
from Definition import Definition
from pathlib import Path
import json

class Synset:
    # Some synsets are created, but not selected during the decomposition process. We do not want these.
    cached_synsets: Dict[str, 'Synset'] = {}

    # todo add get or create via __new__

    def __init__(self, synset_id: str, definition: str, pos: str):
        self.synset_id: str = synset_id
        self.word: str = synset_id.split(".")[0]
        self.definition: Definition = Definition(definition)
        self.pos: str = pos

    @classmethod
    def from_dictionary_object(cls, synset_id: str, definition: Definition, pos: str):
        synset = cls(synset_id, "", pos)
        synset.definition = definition
        return synset

    def __repr__(self) -> str:
        return "Synset(synset_id={}, pos={}, definition={})".format(self.synset_id, self.pos, self.definition)
    
    def __str__(self) -> str:
        return f"{self.word} ({self.pos}): {self.definition}"
    
    @classmethod
    def save_cache(cls):
        with open("cache.json", "w") as f:
            json.dump(cls.all_to_dict(), f, indent=3)

    @classmethod
    def load_cache(cls):
        if not Path("cache.json").exists():
            return
        
        with open("cache.json", "r") as f:
            cache = json.load(f)
            for synset_id, synset_dict in cache.items():
                cls.cached_synsets[synset_id] = Synset.from_dict(synset_dict)

    @classmethod
    def from_wn_synset(cls, synset_id: str):
        synset = wn.synset(synset_id)
        #lemmas = synset.Lemmas()
        return cls(synset.name(), synset.definition(), synset.pos()) # type: ignore

    @classmethod
    def all_to_dict(cls) -> Dict[str, Any]:
        return {synset_id: synset.to_dict() for (synset_id, synset) in Synset.cached_synsets.items()}

    @classmethod
    def all_to_stringy_json(cls) -> str:
        all_json = cls.all_to_dict()
        return json.dumps(all_json, indent=4)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "synset_id": self.synset_id,
            "pos": self.pos,
            "definition": self.definition.to_dict(),
        }
    
    @classmethod
    def from_dict(cls, synset_dict: Dict[str, Any]) -> Self:
        return cls.from_dictionary_object(
            synset_id=synset_dict["synset_id"],
            definition=Definition.from_dict(synset_dict["definition"]),
            pos=synset_dict["pos"]
        )