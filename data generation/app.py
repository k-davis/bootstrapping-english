from Conjugation import Conjugation
from Synset import Synset

def disambiguation_loop():
    # get the starting word
    inp = input("Starting conjugated word: ")
    starting_conjugation = Conjugation(inp)
    
    synset = get_user_decided_meaning_of_conjugation(starting_conjugation)
    if synset is None:
        print("No synsets found for the starting conjugation.")
        return
    
    for idx, token in synset.definition.interesting_tokens():
        # disambiguate each interesting token in the definition
        definition_synset = get_user_decided_meaning_of_conjugation(Conjugation(token))
        if definition_synset is None:
            continue

        synset.definition.decomposition[idx] = definition_synset.synset_id

    print()
    print("Summary:")
    print("Starting word: {}".format(starting_conjugation))
    print("As in: {}".format(synset))

    print()
    print("Definition decomposition:")
    for idx, synset_id in synset.definition.decomposition.items():
        print(" '{}' as in {}".format(synset.definition.definition_tokens[idx], synset_id))

    synset.definition.is_decomposed = True

    print(Synset.all_to_stringy_json())

def get_user_decided_meaning_of_conjugation(conjugation: Conjugation) -> Synset | None:
    possible_synsets = conjugation.possible_synsets()
    if len(possible_synsets) == 0:
        print(f"No synsets found for '{conjugation}'.")
        return None
              
    print("Pick a meaning for '{}':".format(conjugation))
    for i, synset in enumerate(possible_synsets):
        print(" {}. {}".format(i, synset))

    synset_index_response = input("Index: ")
    if synset_index_response == "skip":
        return None
    
    synset_index = int(synset_index_response)
    
    print()

    selected_synset = possible_synsets[synset_index]
    Synset.cached_synsets[selected_synset.synset_id] = selected_synset

    return selected_synset

if __name__ == "__main__":
    Synset.load_cache()
    disambiguation_loop()
    Synset.save_cache()
