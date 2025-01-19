import sys
from csv_reader import read_graph_from_csv
from graph_converter import convert_to_dfa
from csv_writer import write_graph_to_csv

def main(input_file, output_file):
    graph = read_graph_from_csv(input_file)
    print("Graph:", graph)
    dfa_graph = convert_to_dfa(graph)
    write_graph_to_csv(dfa_graph, output_file)

if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("main.exe <input_file.csv> <output_file.csv>")
    #     sys.exit(1)

    # input_file, output_file = sys.argv[1], sys.argv[2]
    input_file = "D:\\Repos\\Github\\taifya\\lab4-python\\dist\\tests\\test.csv"
    output_file = "D:\\Repos\\Github\\taifya\\lab4-python\\dist\\tests\\output.csv"
    main(input_file, output_file)