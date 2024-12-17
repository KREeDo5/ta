import copy
from collections import defaultdict

class MealyMachine:
    def __init__(self):
        self.transitions = {}
        self.outputs = {}

    def add_transition(self, state, input_symbol, next_state, output):
        self.transitions[(state, input_symbol)] = next_state
        self.outputs[(state, input_symbol)] = output

    def get_output(self, state, input_symbol):
        return self.outputs.get((state, input_symbol), None)

    def get_next_state(self, state, input_symbol):
        return self.transitions.get((state, input_symbol), None)

    def __str__(self):
        result = "Mealy Machine:\n"
        for (state, input_symbol), next_state in self.transitions.items():
            output = self.outputs[(state, input_symbol)]
            result += f"From state {state}, on input '{input_symbol}', go to {next_state} with output '{output}'\n"
        return result


class MooreMachine:
    def __init__(self):
        self.transitions = {}
        self.state_outputs = {}

    def add_state_output(self, state, output):
        self.state_outputs[state] = output

    def add_transition(self, state, input_symbol, next_state):
        self.transitions[(state, input_symbol)] = next_state

    def get_output(self, state):
        return self.state_outputs.get(state, None)

    def get_next_state(self, state, input_symbol):
        return self.transitions.get((state, input_symbol), None)

    def __str__(self):
        result = "Moore Machine:\n"
        for (state, input_symbol), next_state in self.transitions.items():
            output = self.state_outputs[next_state]
            result += f"From state {state}, on input '{input_symbol}', go to {next_state} with output '{output}'\n"
        return result


class Minimizer:
    def __init__(self):
        pass

    def minimize_mealy(self, machine):
        # Placeholder for Mealy machine minimization logic
        print("Minimizing Mealy machine (functionality not fully implemented yet).")
        return machine

    def minimize_moore(self, machine):
        # Placeholder for Moore machine minimization logic
        print("Minimizing Moore machine (functionality not fully implemented yet).")
        return machine


def read_mealy_machine(file_path):
    machine = MealyMachine()
    with open(file_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 4:
                state, input_symbol, next_state, output = parts
                machine.add_transition(state, input_symbol, next_state, output)
    return machine

def read_moore_machine(file_path):
    machine = MooreMachine()
    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 2:
                state, output = parts
                machine.add_state_output(state, output)
            elif len(parts) == 3:
                state, input_symbol, next_state = parts
                machine.add_transition(state, input_symbol, next_state)
    return machine

def main():
    # Example of reading and displaying a Mealy machine
    mealy_machine = read_mealy_machine("mealy_input.txt")
    print(mealy_machine)

    # Example of reading and displaying a Moore machine
    moore_machine = read_moore_machine("moore_input.txt")
    print(moore_machine)

    # Minimization examples (placeholder functionality)
    minimizer = Minimizer()
    minimized_mealy = minimizer.minimize_mealy(mealy_machine)
    print("Minimized Mealy Machine:\n", minimized_mealy)

    minimized_moore = minimizer.minimize_moore(moore_machine)
    print("Minimized Moore Machine:\n", minimized_moore)


if __name__ == "__main__":
    main()
