import re #для работы с регулярными выражениями

def parse_grammar(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    print(lines)

    rules = {}
    grammar_type = None

    for line in lines:
        match = re.match(r'<(\w+)> -> (.+)', line)
        if match:
            non_terminal = match.group(1)
            productions = match.group(2).split('|')
            rules[non_terminal] = [prod.strip() for prod in productions]
            # Определяем тип грамматики
            if grammar_type is None:
                grammar_type = 'left' if '<' in productions[0].split()[0] else 'right'

    return grammar_type, rules
