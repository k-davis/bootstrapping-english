from __future__ import annotations
from typing import Dict, Any

import json
from pathlib import Path
import Synset

class SynsetCache:
    def __init__(self, filename):
        self.cache = {}
        self.filename = filename

    def get(self, synset_id: str) -> Synset.Synset | None:
        """Get a synset from the cache by its ID. Returns None if not found."""
        return self.cache.get(synset_id)

    def set(self, synset: Synset.Synset):
        """Add or update the synset in the cache"""
        self.cache[synset.synset_id] = synset

    def __iter__(self):
        return iter(self.cache.values())

    def __contains__(self, synset_id: str):
        return synset_id in self.cache

    def save_to_file(self):
        with open(self.filename, "w") as f:
            json.dump(self.to_dict(), f, indent=3)

    def load_from_file(self):
        if not Path(self.filename).exists():
            return
        
        with open(self.filename, "r") as f:
            cache = json.load(f)
            for synset_id, synset_dict in cache.items():
                self.set(Synset.Synset.from_dict(synset_dict))


    def to_dict(self) -> Dict[str, Any]:
        return {synset_id: synset.to_dict() for (synset_id, synset) in self.cache.items()}

    def to_stringy_json(self) -> str:
        all_json = self.to_dict()
        return json.dumps(all_json, indent=4)
