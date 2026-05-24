
class Definition:
    def __init__(self, definition: str):
        self.definition_text: str = definition
        self.definition_tokens: list[str] = self.tokenize_definition(definition)
        # maps an index in the definition tokens (all) to a synset_id
        self.decomposition: dict[int, str] = {}
        self.is_decomposed: bool = False

    def tokenize_definition(self, definition: str) -> list[str]:
        tokens = definition.split(" ")
        tokens = [token.strip(",.()\"") for token in tokens]
        return tokens

    # Returns the index within the original definition
    def interesting_tokens(self) -> list[tuple[int, str]]:
        boring_tokens = set(["a", "an",
                             "the", 
                             "for", "and", "nor", "but", "or", "yet", "so",
                             "this", "that", "these", "those",
                             "is", "are", "was", "were", 
                             "in", "on", "at", "of"])
        
        all_enumerated_tokens = enumerate(self.definition_tokens)
        return [(i, token) for i, token in all_enumerated_tokens if token not in boring_tokens]

    def __str__(self) -> str:
        return self.definition_text
    
    def to_dict(self) -> dict:
        return {
            "definition_text": self.definition_text,
            "decomposition": self.decomposition if self.is_decomposed else None,
        }
    
    @classmethod
    def from_dict(cls, definition_dict: dict) -> 'Definition':
        definition = cls(definition_dict["definition_text"])
        if definition_dict["decomposition"] is not None:
            definition.decomposition = definition_dict["decomposition"]
            definition.is_decomposed = True
        return definition
    
    