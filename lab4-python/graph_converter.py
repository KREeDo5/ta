import networkx as netx

def convert_to_dfa(nfa):
    dfa = netx.DiGraph()

    start_state = nfa.graph['start']  # Получаем начальное состояние NFA
    print("начальное состояние:", start_state)

    epsilon_closure = get_epsilon_closure(nfa, {start_state}) # Вычисляем ε-замыкание начального состояния
    print("ε-замыкание начального состояния:", epsilon_closure)

    # Используем очередь для обработки новых состояний DFA
    state_queue = [frozenset(epsilon_closure)]
    dfa_states = {frozenset(epsilon_closure): 'S0'}  # отображение набора NFA-состояний в DFA-состояния
    dfa.graph['start'] = 'S0'
    dfa_counter = 1

    print(f"Начальное состояние DFA: {dfa_states[frozenset(epsilon_closure)]} с ε-замыканием: {epsilon_closure}")

    while state_queue:
        current_set = state_queue.pop(0)
        current_dfa_state = dfa_states[current_set]

        print("current_dfa_state:", current_dfa_state)

        # Проверяем финальность текущего состояния
        is_final = any(nfa.nodes[state].get('is_final', False) for state in current_set)
        dfa.add_node(current_dfa_state, is_final=is_final)

        print(f"Текущее состояние DFA: {current_dfa_state}, включает NFA состояния: {current_set}, финальное: {is_final}")

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
            print("ε-замыкание полученного состояния:", epsilon_closure_next)
            next_set = frozenset(epsilon_closure_next)

            if next_set not in dfa_states:
                dfa_states[next_set] = f'S{dfa_counter}'
                state_queue.append(next_set)
                print(f"Новое состояние DFA: {dfa_states[next_set]} с ε-замыканием: {epsilon_closure_next}")
                dfa_counter += 1

            # Добавляем переход в DFA
            dfa.add_edge(current_dfa_state, dfa_states[next_set], in_signal=signal)
            print(f"Добавлен переход: {current_dfa_state} --{signal}--> {dfa_states[next_set]}")

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
