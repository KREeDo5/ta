import networkx as netx

def convert_to_dfa(nfa):
    # Создаем пустой граф для DFA
    dfa = netx.DiGraph()

    # Получаем начальное состояние NFA
    start_state = nfa.graph['start']

    # Вычисляем ε-замыкание начального состояния
    epsilon_closure = get_epsilon_closure(nfa, {start_state})

    # Используем очередь для обработки новых состояний DFA
    state_queue = [frozenset(epsilon_closure)]
    dfa_states = {frozenset(epsilon_closure): 'q0'}  # отображение набора NFA-состояний в DFA-состояния
    dfa.graph['start'] = 'q0'
    dfa_counter = 1

    while state_queue:
        current_set = state_queue.pop(0)
        current_dfa_state = dfa_states[current_set]

        # Определяем финальность текущего состояния
        is_final = any(nfa.nodes[state].get('is_final', False) for state in current_set)
        dfa.add_node(current_dfa_state, is_final=is_final)

        # Получаем все возможные сигналы (кроме ε)
        signals = set(edge_data['in_signal'] for state in current_set
                      for _, _, edge_data in nfa.out_edges(state, data=True)
                      if edge_data['in_signal'] != 'ε')

        for signal in signals:
            # Собираем все состояния, достижимые по сигналу
            next_states = set()
            for state in current_set:
                for _, to_state, edge_data in nfa.out_edges(state, data=True):
                    if edge_data['in_signal'] == signal:
                        next_states.add(to_state)

            # Рассчитываем ε-замыкание для полученных состояний
            epsilon_closure_next = get_epsilon_closure(nfa, next_states)
            next_set = frozenset(epsilon_closure_next)

            if next_set not in dfa_states:
                dfa_states[next_set] = f'q{dfa_counter}'
                state_queue.append(next_set)
                dfa_counter += 1

            # Добавляем переход в DFA
            dfa.add_edge(current_dfa_state, dfa_states[next_set], in_signal=signal)

    return dfa

def get_epsilon_closure(nfa, states):
    closure = set(states)
    stack = list(states)

    while stack:
        state = stack.pop()
        for _, to_state, edge_data in nfa.out_edges(state, data=True):
            if edge_data['in_signal'] == 'ε' and to_state not in closure:
                closure.add(to_state)
                stack.append(to_state)

    return closure