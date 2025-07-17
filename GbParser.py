import graphbrain.parsers as pr
import graphbrain.notebook as nb

# takes about 20 seconds
parser = pr.create_parser(lang='en')

def parse(string):
    parses = parser.parse(string)['parses']
    for parse in parses:
        edge = parse['main_edge']
        print(edge.to_str())
    return parses[0]['main_edge']

results = parser.parse("The quick brown fox jumps over the lazy dog. The dog didn't like it.")
