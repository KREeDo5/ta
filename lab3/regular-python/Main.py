import sys
from grammar_reader import read_grammar
from graph_converter import convert_to_graph
from csv_writer import write_graph_to_csv


def main(input_file, output_file):
    success, grammar, is_left = read_grammar(input_file)
    if not success:
        print("Ошибка записи грамматики")
        sys.exit(1)

    graph = convert_to_graph(grammar, is_left)
    write_graph_to_csv(graph, output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("main.exe <input_file.txt> <output_file.csv>")
        sys.exit(1)

    input_file, output_file = sys.argv[1], sys.argv[2]
    main(input_file, output_file)
