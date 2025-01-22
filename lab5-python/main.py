from validator import valid_brackets
from graph import Graph

def getAlphabet(reg):
    return set(reg) - set('()|*+')

def replace_eps_epsilon(input_str):
    return input_str.replace('eps', 'ε').replace('e', 'ε')

# (abc)*(ab)*
# (a.c)*(a.)*
# (abc)*a*b*
# ((ab|aab)*a*)*
# ((b+a)*b|ε)b*
# ((a|-)((dd*.d*)|(d*.dd*)))|(((dd*.d*)|(d*.dd*)))
# (((dd*.d*)|(d*.dd*)))
input = '(((dd*.d*)|eps))'

input = replace_eps_epsilon(input)

if not valid_brackets(input, True):
    exit(1)
alphabet = None

regex = input + '#'
alphabet = getAlphabet(regex)
#print('Алфавит: ' + ''.join(sorted(alphabet)))
graph = Graph(regex, alphabet)
dfa = graph.toDfa(alphabet)
dfa.write()