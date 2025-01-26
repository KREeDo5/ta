import sys
from lexer import Lexer, LexerError

def main(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as file:
        text = file.read()

    output_code_filename =  './code_output.txt'   

    lx = Lexer()
    lx.input(text)

    tokenList = list(lx.tokens())

    with open(output_code_filename, 'w', encoding='utf-8') as output_code_file:
        for token in tokenList:
            output_code_file.write(str(token) + '\n')

    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for token in tokenList:
            if token.type != 'comment':
                output_file.write(str(token) + '\n')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Введите: main.exe <input_filename> <output_filename>")
    else:
        main(sys.argv[1], sys.argv[2])