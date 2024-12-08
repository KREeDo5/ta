import csv

def save_to_csv(transitions, final_state, output_file):
    states = sorted(transitions.keys())
    terminals = sorted({t for tr in transitions.values() for t in tr.keys()})
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        # Заголовки
        writer.writerow([''] + terminals + ['F'])
        # Переходы
        for state in states:
            row = [state]
            for terminal in terminals:
                row.append(','.join(transitions[state].get(terminal, [])))
            row.append('F' if state == final_state else '')
            writer.writerow(row)
