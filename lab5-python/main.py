def getAlphabet(reg):
    return set(reg) - set('()|*+')

def valid_brackets(regex):
    opened_brackets = 0
    for c in regex:
        if c == '(':
            opened_brackets += 1
        if c == ')':
            opened_brackets -= 1
        if opened_brackets < 0:
            print('Пропущены открывающие скобки!')
            return False
    if opened_brackets == 0:
        return True
    print('Пропущены открывающие скобки')
    return False

# (abc)*(ab)*
# (abc)*a*b*
# ((ab|aab)*a*)*
input = '((ab|aab)*a*)*'

if not valid_brackets(input):
    exit(1)
alphabet = None

regex = input + '#'
print('regex : ' + regex)
alphabet = getAlphabet(regex)

#строить дерево