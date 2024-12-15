import re
import networkx as netx

LEFT_RULE = r'\s*(?:<(\w+)>\s+)?([\wε])\s*'
RIGHT_RULE = r'\s*([\wε])(?:\s+<(\w+)>)?\s*'
FINAL_SIGNAL = 'F'
ARTIFICIAL_STATE = ''


def is_state(map, state):
    if state in map.keys():
        return map[state]
    else:
        print(f'Rule for state <{state}> not found')
        return None

def convert_to_graph(grammar, is_left):
    graph = netx.MultiDiGraph()
    states = [rule[0] for rule in grammar] + [ARTIFICIAL_STATE]
    if is_left:
        states.reverse()
    state_mapping = {state: f'q{i}' for i, state in enumerate(states)}

    artificial_state = 'H' if is_left else 'F'
    for key, value in state_mapping.items():
        old_state = artificial_state if key == ARTIFICIAL_STATE else key
        print(f'{old_state} -> {value}')

    for state in states:
        graph.add_node(state_mapping[state], out_signal=FINAL_SIGNAL if state == states[-1] else '')

    regex = re.compile(LEFT_RULE if is_left else RIGHT_RULE)

    for rules in grammar:
        if is_left:
            to_state = state_mapping[rules[0]]
        else:
            from_state = state_mapping[rules[0]]

        rules = [match.groups() for match in regex.finditer(rules[1])]

        for rule in rules:
            if is_left:
                in_signal = rule[1]
                from_state = state_mapping[ARTIFICIAL_STATE] if rule[0] is None else is_state(state_mapping, rule[0])
            else:
                in_signal = rule[0]
                to_state = state_mapping[ARTIFICIAL_STATE] if rule[1] is None else is_state(state_mapping, rule[1])

            if from_state is None or to_state is None:
                return None
            graph.add_edge(from_state, to_state, in_signal=in_signal)

    return graph

