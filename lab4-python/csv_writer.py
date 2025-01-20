import csv

def write_graph_to_csv(graph, file_path):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')

        states = list(graph.nodes)
        print("States:", states)

        signals = sorted(
            set(edge_data['in_signal'] for _, _, edge_data in graph.edges(data=True) if edge_data['in_signal'] and edge_data['in_signal'] != 'ε')
        )
        print("Signals:", signals)

        # Определение финальных состояний
        final_states = [state for state in states if graph.nodes[state].get('is_final', False)]
        print("Final States:", final_states)

        # Запись первой строки с индикацией финальных состояний
        writer.writerow([''] + ['F' if state in final_states else '' for state in states])

        # Запись второй строки с именами состояний
        writer.writerow([''] + states)

        # Запись переходов
        for signal in signals:
            row = [signal] + ['' for _ in states]
            for from_state, to_state, edge_data in graph.edges(data=True):
                if edge_data['in_signal'] == signal:
                    index = states.index(from_state)
                    if row[index + 1]:
                        row[index + 1] += f',{to_state}'
                    else:
                        row[index + 1] = to_state
            writer.writerow(row)