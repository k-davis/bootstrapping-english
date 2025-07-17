from Term import *
from pywsd import disambiguate 

class Corpus:
    def __init__(self, text):
        self.text = text
        
        # In the form of Tuple(word, lemma, synset)
        raw_disambiguated_words: list[tuple[unknown, unknown, unknown]] = disambiguate(text, similarity_option='wup', keepLemmas=True) # type: ignore
        self.disambiguated_words = []
        for term in raw_disambiguated_words:
            if term[0] is None:
                continue
            if term[0] in "`!@#$%^&*()_+-=[]{}|;':\",.<>?/~`“”":
                continue

            cleaned_word = term[0].strip('_')
            cleaned_lemma = term[1].strip('_')

            new_term = Term(cleaned_word, cleaned_lemma, term[2])
            self.disambiguated_words.append(new_term)

        self.lemma_to_words = {}
        for term in self.disambiguated_words:
            if term.lemma not in self.lemma_to_words:
                self.lemma_to_words[term.lemma] = set()
            self.lemma_to_words[term.lemma].add(term.word)

        self.synset_to_lemmas = {}
        for term in self.disambiguated_words:
            if term.synset is None:
                continue

            if term.synset not in self.synset_to_lemmas:
                self.synset_to_lemmas[term.synset] = set()
            self.synset_to_lemmas[term.synset].add(term.lemma)

    def __repr__(self):
        return f"Corpus({self.text})"

    def unique_words(self):
        unique_words = set(term.word.lower() for term in self.disambiguated_words)
        return unique_words

    def word_count(self):
        return len(self.disambiguated_words)

    def unique_lemmas(self):
        return set(term.lemma for term in self.disambiguated_words)
    
    # Does not include functional words
    def unique_synsets(self):
        return set(term.synset for term in self.disambiguated_words)

    def unique_lemmas_without_synsets(self):
        unique_lemmas = set()
        for term in self.disambiguated_words:
            if term.synset is None:
                unique_lemmas.add(term.lemma)

        return unique_lemmas
