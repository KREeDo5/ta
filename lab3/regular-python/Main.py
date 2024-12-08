from Parse import parse_grammar
from GrammarToNFA import grammar_to_nfa
from SaveCSV import save_to_csv

def main(input_file, output_file):
    grammar_type, rules = parse_grammar(input_file)
    transitions, final_state, state_map = grammar_to_nfa(grammar_type, rules)
    save_to_csv(transitions, final_state, output_file)
    print("Состояния:")
    for non_terminal, state in state_map.items():
        print(f"{non_terminal} -> {state}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Введите: main.exe tests/input.txt tests/output.csv")
    else:
        main(sys.argv[1], sys.argv[2])

