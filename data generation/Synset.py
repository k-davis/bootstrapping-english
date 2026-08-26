from __future__ import annotations
import copy
from typing import Any, Dict
from typing_extensions import Self
from nltk.corpus import wordnet as wn 
from Definition import Definition
import src.models.SynsetCache

class Synset:
    # Some synsets are created, but not selected during the decomposition process. We do not want these.
    #cached_synsets: Dict[str, 'Synset'] = {}
    wn_cache: src.models.SynsetCache.SynsetCache
    cur_decomposition_cache: src.models.SynsetCache.SynsetCache
    # TODO add get or create via __new__

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
    def from_wn_synset(cls, synset_id: str):
        # try to read from cache
        if synset_id in cls.cur_decomposition_cache:
            return cls.cur_decomposition_cache.get(synset_id)
        elif synset_id in cls.wn_cache:
            return cls.wn_cache.get(synset_id)

        else:
            wn_synset = wn.synset(synset_id)
            new_synset = cls(wn_synset.name(), wn_synset.definition(), wn_synset.pos()) # type: ignore
            cls.wn_cache.set(copy.deepcopy(new_synset))
            return new_synset
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "synset_id": self.synset_id,
            "pos": self.pos,
            "definition": self.definition.to_dict() if self.definition else None,
        }
    
    @classmethod
    def from_dict(cls, synset_dict: Dict[str, Any]) -> Self:
        return cls.from_dictionary_object(
            synset_id=synset_dict["synset_id"],
            definition=Definition.from_dict(synset_dict["definition"]),
            pos=synset_dict["pos"]
        )