import csv
import networkx as netx

def read_graph_from_csv(file_path):
    graph = netx.MultiDiGraph()
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        rows = list(reader)
        print("Rows:", rows)

        #1 строка - индикация финальных состояний
        final_states = set()
        if 'F' in rows[0]:
            final_states = set(rows[1][i] for i, cell in enumerate(rows[0]) if cell == 'F')

        print("финальные состояния:", final_states)

        #2 строка - список состояний автомата.
        states = rows[1][1:]
        for state in states:
            graph.add_node(state, is_final=(state in final_states))

        print("список состояний:", states)

        start_state = states[0]  # первое состояние - начальное
        graph.graph['start'] = start_state

        print("начальное состояние:", start_state)

        # Остальные строки - переходы между состояниями
        for row in rows[2:]:
            signal = row[0] # Входной сигнал
            print("входной сигнал:", signal)
            for i, transitions in enumerate(row[1:], start=1):
                if transitions:
                    from_state = states[i - 1]
                    print("переход из состояния:", from_state)
                    for to_state in transitions.split(','):
                        # Несколько переходов по одному символу разделяются запятой.
                        print("переход в состояниe:", to_state)
                        graph.add_edge(from_state, to_state, in_signal=signal)

    return graph