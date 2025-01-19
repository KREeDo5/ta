import networkx as netx

def convert_to_dfa(nfa):
    dfa = netx.MultiDiGraph()
    start_state = frozenset([nfa.graph['start']])
    dfa.add_node(start_state)
    unmarked_states = [start_state]
    marked_states = set()

    while unmarked_states:
        current = unmarked_states.pop()
        marked_states.add(current)
        for symbol in set(edge_data['in_signal'] for _, _, edge_data in nfa.edges(data=True)):
            new_state = frozenset(
                state for s in current for state in nfa.successors(s) if nfa[s][state][0]['in_signal'] == symbol
            )
            if new_state not in marked_states:
                unmarked_states.append(new_state)
            dfa.add_node(new_state)
            dfa.add_edge(current, new_state, in_signal=symbol)

    return dfa