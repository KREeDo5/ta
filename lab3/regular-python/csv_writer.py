import csv

def write_graph_to_csv(graph, file_path):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')

        states = list(graph.nodes)
        print("States:", states)

        signals = sorted(
            set(edge_data['in_signal'] for _, _, edge_data in graph.edges(data=True) if edge_data['in_signal'] is not None)
        )
        print("Signals:", signals)

        # Записываем первую строку заголовка с F
        writer.writerow([''] + ['' for _ in states] + ['F'])

        # Записываем вторую строку заголовка с названиями состояний
        writer.writerow([''] + states)

        # Для каждого сигнала составляем строку
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