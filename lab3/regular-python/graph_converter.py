import re
import networkx as netx

LEFT_RULE = r'\s*(?:<(\w+)>\s+)?([\wε])\s*'
RIGHT_RULE = r'\s*([\wε])(?:\s+<(\w+)>)?\s*'
FINAL_SIGNAL = 'F'
EMPTY_STATE = ''


def is_state(map, state):
    if state in map.keys():
        return map[state]
    print(f'Правило для <{state}> не найдено')
    return None

def get_state(rule, state_map):
    return state_map[EMPTY_STATE] if rule is None else is_state(state_map, rule)

def convert_to_graph(grammar, is_left):
    graph = netx.MultiDiGraph()
    states = [rule[0] for rule in grammar] + [EMPTY_STATE]

    if is_left:
        states.reverse()

    state_map = {state: f'q{i}' for i, state in enumerate(states)}

    placeholder  = 'H' if is_left else 'F'

    for key, value in state_map.items():
        old_state = placeholder if key == EMPTY_STATE else key
        print(f'{old_state} -> {value}')

    for state in states:
        graph.add_node(state_map[state], out_signal=FINAL_SIGNAL if state == states[-1] else '')

    regex = re.compile(LEFT_RULE if is_left else RIGHT_RULE)

    for rules in grammar:
        state = state_map[rules[0]]

        rules = [match.groups() for match in regex.finditer(rules[1])]

        for rule in rules:
            if is_left:
                signal = rule[1]
                target_state = state
                source_state = get_state(rule[0], state_map)
            else:
                signal = rule[0]
                source_state = state
                target_state = get_state(rule[1], state_map)

            if source_state is None or target_state is None:
                return None

            graph.add_edge(source_state, target_state, in_signal=signal)

    return graph

