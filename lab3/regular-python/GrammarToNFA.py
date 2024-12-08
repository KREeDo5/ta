def grammar_to_nfa(grammar_type, rules):
    state_map = {non_terminal: f'q{i}' for i, non_terminal in enumerate(rules.keys())}
    transitions = {state: {} for state in state_map.values()}
    final_state = f'q{len(rules)}'

    for non_terminal, productions in rules.items():
        for prod in productions:
            parts = prod.split()
            if grammar_type == 'left':
                # Левосторонняя: терминал в конце
                terminal, target = parts[-1], parts[0] if len(parts) > 1 else final_state
            else:
                # Правосторонняя: терминал в начале
                terminal, target = parts[0], parts[1] if len(parts) > 1 else final_state

            state = state_map[non_terminal]
            target_state = state_map.get(target, final_state)
            if terminal not in transitions[state]:
                transitions[state][terminal] = []
            transitions[state][terminal].append(target_state)

    return transitions, final_state, state_map
