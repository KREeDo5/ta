import sys
from lexer import Lexer, LexerError

def main(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as file:
        text = file.read()

    lx = Lexer()
    lx.input(text)

    try:
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            for token in lx.tokens():
                output_file.write(str(token) + '\n')
    except LexerError as errorString:
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write(str(errorString) + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Введите: main.exe <input_filename> <output_filename>")
    else:
        main(sys.argv[1], sys.argv[2])