import sys
import re
# Оформление грамматики
# \d          | 0-9 (любая ЦИФРА - не число)
# \.          | соответствует точке в качестве литерала, а не символа.
# .           | любой символ
# \w          | а–я, А–Я, 0–9 или _
# ?           | предыдущий символ или выражение могут быть в строке 0 или 1 раз (не * Клини)
# [:punct:]   | знаки: ! " # $ % & ' ( ) * + , \ -. / : ; < = > ? @ [ ] ^ _ ` { | }

def lex_results(pattern, text, type):
    results = []
    for lineNum, line in enumerate(text, start=1):
        for match in pattern.finditer(line):
            token = None
            if match.lastgroup:
                token = match.lastgroup
            results.append({
                'token': token,
                'type': type,
                'item': match.group(),
                'line': lineNum,
                'pos': match.start() + 1
            })
    return results

def lex_identifiers(text):
    identifiers_pattern = re.compile(r'''
        (?P<private>_[a-zA-Z0-9][_a-zA-Z0-9]*)
        |(?P<public>[a-zA-Z][_a-zA-Z0-9]*)
    ''', re.VERBOSE)

    return lex_results(identifiers_pattern, text, 'id')

def lex_numbers(text):
    number_pattern = re.compile(r'''
        (?<!\w)  # Граница: перед числом не должно быть буквы/цифры
        (?P<binary>0b[01]+)                       # Двоичные числа (0b101)
        |(?P<octal>0o[0-7]+)                      # Восьмеричные числа (0o71)
        |(?P<hexadecimal>0x[\da-fA-F]+)           # Шестнадцатеричные числа (0x1A45F0D)
        |(?P<float>\d+\.\d+)                      # Числа с плавающей точкой (123.456)
        |(?P<scientific_float>\d+\.\d+e[+-]?\d+)  # Числа в научной нотации с точкой (123.456e+8)
        |(?P<scientific>\d+e[+-]?\d+)             # Числа в научной нотации (1e-8)
        |(?P<decimal>\d+)                         # Десятичные целые числа (123)
        (?!\w) # Граница: после числа не должно быть буквы/цифры
    ''', re.VERBOSE)
    return lex_results(number_pattern, text, 'number')

def lex_conditions(text):
    conditions_pattern = re.compile(r'''
        \b # Граница слова
        (?P<int>int)
        |(?P<double>double)
        |(?P<char>char)
        |(?P<string>string)
        |(?P<bool>bool)
        |(?P<if>if)
        |(?P<while>while)
        |(?P<for>for)
        |(?P<true>true)
        |(?P<false>false)
        \b # Граница слова
    ''', re.VERBOSE)

    return lex_results(conditions_pattern, text, 'condition')

def lex_operators(text):
    operators_pattern = re.compile(r'''
        (?<!/)     # Перед оператором не должно быть символа / (негативный просмотр назад)
        (?<!\*)    # Перед оператором не должно быть символа *
        (?P<plus>\+)
        |(?P<minus>\-)
        |(?P<multiply>\*)
        |(?P<divide>/)
        |(?P<module>%)
        |(?P<not_equal>!=)
        |(?P<equal>==)
        |(?P<less_equal><=)
        |(?P<greater_equal>>=)
        |(?P<less><)
        |(?P<greater>>)
        (?!/)      # После оператора не должно быть символа /
        (?!\*)     # После оператора не должно быть символа *
    ''', re.VERBOSE)

    return lex_results(operators_pattern, text, 'operator')

def lex_comments(text):
    comments_pattern = re.compile(r'''
        (?P<single_line>//.*)
        |(?P<multi_line>/\*[\s\S]*?\*/)  #TODO: проверить многострочные комментарии
    ''', re.VERBOSE)

    return lex_results(comments_pattern, text, 'comment')

def lex_brackets(text):
    brackets_pattern = re.compile(r'''
        (?P<bracket_open>\()
        |(?P<bracket_close>\))
        |(?P<brace_open>{)
        |(?P<brace_close>})
        |(?P<bracket_sq_open>\[)
        |(?P<bracket_sq_close>\])
    ''', re.VERBOSE)

    return lex_results(brackets_pattern, text, 'bracket')

def lex_separators(text):
    separators_pattern = re.compile(r'''
        (?P<semicolon>;)
        |(?P<newline>/n)
        |(?P<tab>/t)
    ''', re.VERBOSE)

    return lex_results(separators_pattern, text, 'separator')

def main(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    string = text.splitlines()  #разбиваю текст на множество строк

    numbers = lex_numbers(string)
    comments = lex_comments(string)
    conditions = lex_conditions(string)
    brackets = lex_brackets(string)
    separators = lex_separators(string)
    operators = lex_operators(string)
    identifiers = lex_identifiers(string)

    for number in numbers:
        print(f"line {number['line']} pos {number['pos']} {number['token']}: '{number['item']}' ")

    for comment in comments:
        print(f"line {comment['line']} pos {comment['pos']} {comment['token']}: '{comment['item']}' ")

    for condition in conditions:
        print(f"line {condition['line']} pos {condition['pos']} {condition['token']}: '{condition['item']}' ")

    for bracket in brackets:
        print(f"line {bracket['line']} pos {bracket['pos']} {bracket['token']}: '{bracket['item']}' ")

    for separator in separators:
        print(f"line {separator['line']} pos {separator['pos']} {separator['token']}: '{separator['item']}' ")

    for operator in operators:
        print(f"line {operator['line']} pos {operator['pos']} {operator['token']}: '{operator['item']}' ")

    for identifier in identifiers:
        print(f"line {identifier['line']} pos {identifier['pos']} {identifier['token']}: '{identifier['item']}' ")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: main.exe <filename>")
    else:
        main(sys.argv[1])