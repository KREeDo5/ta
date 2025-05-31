import sys
import json
from lexer import Lexer

def main(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as file:
        text = file.read()

    lx = Lexer()
    lx.input(text)

    tokenList = list(lx.tokens())


    with open(output_filename, 'w', encoding='utf-8') as json_file:
        json.dump([token.to_dict() for token in tokenList], json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Введите: main.exe <input_filename>.txt <output_filename>.json")
    else:
        main(sys.argv[1], sys.argv[2])