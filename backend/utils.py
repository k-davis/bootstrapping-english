from nltk.corpus import wordnet as wn
from nltk import word_tokenize
from nltk.wsd import lesk

from Synset import Synset

def disambiguate_synsets(word) -> list[Synset]:
    wn_synsets = wn.synsets(word)
    return [Synset(s.name(), s.definition(), s.pos()) for s in wn_synsets]
        

def split_sentence_into_synsets(sentence: str) -> list[Synset]:
    sentence_tokens = word_tokenize(sentence)
    raw_synsets_in_sentence = [lesk(word, sentence) for word in sentence_tokens]
    cleaned_synsets_in_sentence = [Synset.from_wn_synset(s) for s in raw_synsets_in_sentence if s is not None]
    return cleaned_synsets_in_sentence