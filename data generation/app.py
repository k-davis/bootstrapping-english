from Conjugation import Conjugation
from Synset import Synset
from src.models.SynsetCache import SynsetCache
import random

wn_cache: SynsetCache
decomposition_cache: SynsetCache

def main():
    wn_cache = SynsetCache("wn_cache.json")
    decomposition_cache = SynsetCache("decompositions_cache.json")
    wn_cache.load_from_file()
    decomposition_cache.load_from_file()

    Synset.cache = wn_cache

    print("=== Data Generation Tool ===")
    print("Input sanitization is dubious.")
    print(f"{len([s for s in decomposition_cache])} synsets.")
    print(f"{len([s for s in decomposition_cache if not s.definition.is_decomposed])} not yet decomposed.")
    print()

    while True:
        print("Select an action:")
        print(" 0. Decompose a new word (conjugation)")
        print(" 1. Decompose existing, undecomposed synsets")
        print(" 2. Exit")

        selection = input("Selection: ")

        if selection == "0":
            synset = get_new_synset_from_user()
            if synset is None:
                continue
            
            fully_decompose_synset_definition(synset)

        elif selection == "1":
            undecomposed_synsets = [s for s in decomposition_cache if not s.definition.is_decomposed]
            synset_to_decompose = random.choice(undecomposed_synsets)
            fully_decompose_synset_definition(synset_to_decompose)

        elif selection == "2":
            wn_cache.save_to_file()
            decomposition_cache.save_to_file()
            break


def get_new_synset_from_user() -> Synset | None:
    new_word = input("New conjugated word: ")

    synset = get_user_decided_meaning_of_conjugation(Conjugation(new_word))
    #TODO if synset is already in cache and fully decomposed, return
    if synset is None:
        print("No synsets found for the starting conjugation.")
        return

    return synset


def fully_decompose_synset_definition(synset: Synset):
    """
    Prompts the user to select the meaning of each* word in the definition of the given synset
    """
    for idx_into_full_definition, token in synset.definition.interesting_tokens():
        # disambiguate each interesting token in the definition
        print(f"Decomposing definition of {synset.word} ({synset.pos}): {synset.definition}")
        definition_synset = get_user_decided_meaning_of_conjugation(Conjugation(token))
        if definition_synset is None:
            continue

        synset.definition.decomposition[idx_into_full_definition] = definition_synset.synset_id
        decomposition_cache.set(synset)

    synset.definition.is_decomposed = True

    print()

def get_user_decided_meaning_of_conjugation(conjugation: Conjugation) -> Synset | None:
    """Prompts the user to select the meaning (Synset) of a word as used (Conjugation).
    Returns the Synset, or None to go back."""
    possible_synsets = conjugation.possible_synsets()
    if len(possible_synsets) == 0:
        print(f"No synsets found for '{conjugation}'.")
        return None
    elif len(possible_synsets) == 1:
        print(f"Only one synset found for '{conjugation}'")
        return possible_synsets[0]
                  
    print("Pick a meaning for '{}':".format(conjugation))
    for i, synset in enumerate(possible_synsets):
        print(" {}. {}".format(i, synset))

    synset_index_response = input("Selection: ")
    if synset_index_response == "x":
        return None
    
    synset_index = int(synset_index_response)
    
    print()

    selected_synset = possible_synsets[synset_index]
    return selected_synset

if __name__ == "__main__":
    main()
