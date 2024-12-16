import re

LEFT_GRAMMAR = r'^\s*<(\w+)>\s*->\s*((?:<\w+>\s+)?[\wε](?:\s*\|\s*(?:<\w+>\s+)?[\wε])*)\s*$'
RIGHT_GRAMMAR = r'^\s*<(\w+)>\s*->\s*([\wε](?:\s+<\w+>)?(?:\s*\|\s*[\wε](?:\s+<\w+>)?)*)\s*$'


def parse_grammar(text, regex):
    matches = []
    last_position = 0

    for match in re.finditer(regex, text, flags=re.MULTILINE):
        if abs(match.start() - last_position) <= 1:
            matches.append(match.groups())
            last_position = match.end()
        else:
            break
    valid = len(text) == last_position
    result = matches if valid else last_position
    return valid, result


def read_grammar(file_path):
    with open(file_path, encoding='utf-8') as file:
        content = file.read()
        content = content.replace('\t', ' ')

        errors = []
        for grammar_type, regex in [("Left", LEFT_GRAMMAR), ("Right", RIGHT_GRAMMAR)]:
            valid, result = parse_grammar(content, regex)
            if valid:
                return True, result, grammar_type == "Left"
            else:
                error_line = len(content[:result].split('\n')) if isinstance(result, int) else 0
                errors.append((grammar_type, error_line))

        if errors:
            for error in errors:
                print(f'{error[0]}-handed grammar: Ошибка в линии {error[1]}')
        return False, None, None
