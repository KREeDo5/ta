import sys
from grammar_reader import read_grammar
from graph_converter import convert_to_graph
from csv_writer import write_graph_to_csv


def main(input_file, output_file):
    success, grammar, is_left = read_grammar(input_file)
    if not success:
        print("Failed to parse grammar")
        sys.exit(1)

    graph = convert_to_graph(grammar, is_left)
    print(graph)
    print("Nodes:", graph.nodes(data=True))
    print("Edges:", list(graph.edges(data=True)))
    write_graph_to_csv(graph, output_file)
    print("Conversion completed!")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("python main.py <input_file> <output_file>")
        sys.exit(1)

    input_file, output_file = sys.argv[1], sys.argv[2]
    main(input_file, output_file)
