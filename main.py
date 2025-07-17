from Corpus import *
import string

# from pywsd.similarity import max_similarity as maxsim
# import nltk
# from nltk.corpus import wordnet as wn

# # WN documentation
# Synset - a set of synonyms that share a common meaning
# Hypernym - One level up of concept. Or Y is a hypernym of X if every X is also a Y
# Hyponym - One level more specific. Y is hyponym of X if every Y is an X
# Coordinate Item - X is a coordinate item of Y if they share a hypernym
# Holonym - Y of X, when Y has an X
# Meronym - Y of X, when Y is part of X

alice_snippet = ""
with open("text/alice_snippet.txt") as in_file:
    alice_snippet = in_file.read()

s = Corpus(alice_snippet)

print(f"Alice in Wonderland contains {len(s.disambiguated_words)} words.")
print(f"{len(s.unique_words())} are unique.")
print(f"If we ignore conjugation, plurality, and the like, we have {len(s.unique_lemmas())} unique root words, or lemmas.")

print("What lemmas appeared multiple times?")
for lemma, words in s.lemma_to_words.items():
    if len(words) > 2:
        print(f"   {lemma} : {words}")

print(f"If we combine synonyms, and only use one word of the group, then we are left with {len(s.unique_synsets()) + len(set(s.unique_lemmas_without_synsets()))} unique lemmas.")
for synset, lemmas in s.synset_to_lemmas.items():
    if len(lemmas) > 2:
        print(f"   {synset} : {lemmas}")

