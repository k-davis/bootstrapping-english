from graphbrain.parsers import *
parser = create_parser(lang='en')

def parse(string):
    parses = parser.parse(string)['parses']
    for parse in parses:
        edge = parse['main_edge']
        print(edge.to_str())
    return parses[0]['main_edge']