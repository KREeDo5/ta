import sys
from lexer import Lexer, LexerError

def main(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()

    lx = Lexer()
    lx.input(text)

    try:
        for token in lx.tokens():
            print(token)
    except LexerError as errorString:
        print(errorString)

    # for item in code:
    #     print(f"line {item['line']} pos {item['start_pos']} {item['end_pos']} {item['token']}: '{item['item']}' ")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: main.exe <filename>")
    else:
        main(sys.argv[1])