from validator import valid_brackets
from graph import Graph

def getAlphabet(reg):
    return set(reg) - set('()|*+')

# (abc)*(ab)*
# (abc)*a*b*
# ((ab|aab)*a*)*
# ((b+a)*b|ε)b*
# ((a|-)((dd*.d*)|(d*.dd*)))|(((dd*.d*)|(d*.dd*)))
# (((dd*.d*)|(d*.dd*)))
input = '(abc)*(ab)*'

if not valid_brackets(input):
    exit(1)
alphabet = None

regex = input + '#'
print('input : ' + input)
alphabet = getAlphabet(regex)
print('Алфавит: ' + ''.join(sorted(alphabet)))
graph = Graph(regex, alphabet)
dfa = graph.toDfa(alphabet)
dfa.write()