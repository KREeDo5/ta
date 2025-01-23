import sys
from validator import valid_brackets
from graph import Graph

def getAlphabet(reg):
    return set(reg) - set('()|*+')

def replace_eps_epsilon(input_str):
    return input_str.replace('eps', 'ε').replace('e', 'ε')

def main(input_file, output_file):
    with open(input_file, 'r') as file:
        inputStr = file.readline().strip()

    inputStr = replace_eps_epsilon(inputStr)

    if not valid_brackets(inputStr, True):
        exit(1)
    alphabet = None

    regex = inputStr + '#'
    alphabet = getAlphabet(regex)
    # print('Алфавит: ' + ''.join(sorted(alphabet)))
    graph = Graph(regex, alphabet)
    dfa = graph.toDfa(alphabet)
    dfa.to_csv(output_file + '.csv')
    dfa.to_graph(output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: main.exe <input_file> <output_file>")
        exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)