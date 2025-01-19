import csv
import networkx as netx

def read_graph_from_csv(file_path):
    graph = netx.MultiDiGraph()
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        rows = list(reader)

        states = rows[1][1:]
        for state in states:
            graph.add_node(state)

        for row in rows[2:]:
            signal = row[0]
            for i, transitions in enumerate(row[1:], start=1):
                if transitions:
                    from_state = states[i - 1]
                    for to_state in transitions.split(','):
                        graph.add_edge(from_state, to_state, in_signal=signal)

        start_state = states[0]  # Пока что первое состояние является начальным
        graph.graph['start'] = start_state

    return graph