import csv
import networkx as netx

def write_graph_to_csv(graph, file_path):
        with open(file_path, 'w', newline='\n', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            ordered_states = list(graph.nodes)
            indexed_states = dict(zip(ordered_states, range(len(ordered_states))))
            ordered_state_outs = [graph.nodes[node]['out_signal'] for node in ordered_states]
            ordered_signals = sorted(list(set(netx.get_edge_attributes(graph, 'in_signal').values())))
            indexed_signals = dict(zip(ordered_signals, range(len(ordered_signals))))
            writer.writerow([''] + ordered_state_outs)
            writer.writerow([''] + ordered_states)
            transitions_matrix = [[signal] + [''] * len(ordered_states) for signal in ordered_signals]

            for from_state, to_state, edge in graph.edges:
                data = graph.get_edge_data(from_state, to_state, edge)
                signal = data['in_signal']
                state = transitions_matrix[indexed_signals[signal]] \
                    [indexed_states[from_state] + 1]
                transitions_matrix[indexed_signals[signal]] \
                    [indexed_states[from_state] + 1] = to_state if state == '' else f'{state},{to_state}'
            writer.writerows(transitions_matrix)

