import networkx as netx

def convert_to_dfa(nfa):
    dfa = netx.MultiDiGraph()
    start_state = frozenset([nfa.graph['start']])
    state_mapping = {start_state: 'S0'}
    dfa.add_node('S0', is_final=any(nfa.nodes[state]['is_final'] for state in start_state))
    unmarked_states = [start_state]
    marked_states = set()
    state_counter = 1

    while unmarked_states:
        current = unmarked_states.pop()
        marked_states.add(current)
        current_name = state_mapping[current]
        for symbol in set(edge_data['in_signal'] for _, _, edge_data in nfa.edges(data=True) if edge_data['in_signal']):
            new_state = frozenset(
                state for s in current for state in nfa.successors(s) if nfa[s][state][0]['in_signal'] == symbol
            )
            if new_state not in marked_states:
                unmarked_states.append(new_state)
                state_mapping[new_state] = f'S{state_counter}'
                state_counter += 1
            new_state_name = state_mapping[new_state]
            dfa.add_node(new_state_name, is_final=any(nfa.nodes[state]['is_final'] for state in new_state))
            dfa.add_edge(current_name, new_state_name, in_signal=symbol)

    return dfa