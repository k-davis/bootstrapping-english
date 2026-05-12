from Conjugation import Conjugation

if __name__ == "__main__":
    # get the starting word
    inp = input("Starting conjugated word: ")
    starting_conjugation = Conjugation(inp)
    
    # get the intended meaning of the starting word by selecting
    #  the appropriate synset's definition
    possible_synsets = starting_conjugation.possible_synsets()
    
    print("Pick a meaning for {}:".format(starting_conjugation))
    for i, synset in enumerate(possible_synsets):
        print(" {}. {}".format(i, synset.definition))
    synset_index = int(input("Index: "))

    selected_synset = possible_synsets[synset_index]
    print("Selected synset: {}".format(selected_synset))