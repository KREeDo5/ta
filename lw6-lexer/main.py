import sys
import re

# Оформление грамматики
# \d          | 0-9 (любая ЦИФРА - не число)
# \.          | соответствует точке в качестве литерала, а не символа.
# .           | любой символ
# \w          | а–я, А–Я, 0–9 или _
# ?           | предыдущий символ или выражение могут быть в строке 0 или 1 раз (не * Клини)
# [:punct:]   | знаки: ! " # $ % & ' ( ) * + , \ -. / : ; < = > ? @ [ ] ^ _ ` { | }

def lex_numbers(lines):
    number_pattern = re.compile(r'''
        (?<!\w)                 # Граница: перед числом не должно быть буквы/цифры
        (?:                     # Группируем возможные форматы:
            0b[01]+             # Двоичные числа (0b101)
            |0o[0-7]+           # Восьмеричные числа (0o71)
            |0x[\da-fA-F]+      # Шестнадцатеричные числа (0x1A45F0D)
            |\d+\.\d+           # Числа с плавающей точкой (123.456)
            |\d+\.\d+e[+-]?\d+  # Числа в научной нотации с точкой (123.456e+8)
            |\d+e[+-]?\d+       # Числа в научной нотации (1e-8)
            |\d+                # Десятичные целые числа (123)
        )
        (?!\w)                  # Граница: после числа не должно быть буквы/цифры
    ''', re.VERBOSE)

    results = []

    for line_no, line in enumerate(lines, start=1):
        for match in number_pattern.finditer(line):
            results.append({
                'num': match.group(),
                'line': line_no,
                'pos': match.start() + 1  # Позиция начинается с 1
            })

    return results

def main(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    lines = text.splitlines()  #разбиваю текст на множество строк
    results = lex_numbers(lines)

    for result in results:
        print(f"'{result['num']}'       line {result['line']}       pos {result['pos']}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: main.exe <filename>")
    else:
        main(sys.argv[1])