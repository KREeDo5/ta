from graphviz import Digraph

def split_regex(regex):
    components = []
    current_component = []
    open_parentheses = 0

    for char in regex:
        if char == '(':
            open_parentheses += 1
        elif char == ')':
            open_parentheses -= 1
        elif char == '|' and open_parentheses == 0:
            components.append(''.join(current_component))
            current_component = []
            continue

        current_component.append(char)

    if current_component:
        components.append(''.join(current_component))

    return components

def process_component(component, graph, start_state, final_state, state_map):
    if component.endswith('*') or component.endswith('+'):
        operator = component[-1]
        sub_component = component[:-1]
        if sub_component.startswith('(') and sub_component.endswith(')'):
            sub_components = split_regex(sub_component[1:-1])
            for sub_component in sub_components:
                next_state = f"q{len(state_map)}"
                state_map[next_state] = len(state_map)
                graph.edge(f"q{state_map[start_state]}", f"q{state_map[next_state]}", label=sub_component)
                if operator == '*':
                    graph.edge(f"q{state_map[next_state]}", f"q{state_map[next_state]}", label=sub_component)
                    graph.edge(f"q{state_map[start_state]}", f"q{state_map[next_state]}", label='ε')
                    graph.edge(f"q{state_map[next_state]}", f"q{state_map[final_state]}", label='ε')
                    print(f"{sub_component} - зацикливание в состоянии и e-переход перед этим состоянием")
                elif operator == '+':
                    graph.edge(f"q{state_map[next_state]}", f"q{state_map[next_state]}", label=sub_component)
                    graph.edge(f"q{state_map[next_state]}", f"q{state_map[final_state]}", label='ε')
                    print(f"{sub_component} - зацикливание в состоянии и один обязательный переход перед этим состоянием")
        else:
            next_state = f"q{len(state_map)}"
            state_map[next_state] = len(state_map)
            graph.edge(f"q{state_map[start_state]}", f"q{state_map[next_state]}", label=sub_component)
            if operator == '*':
                graph.edge(f"q{state_map[next_state]}", f"q{state_map[next_state]}", label=sub_component)
                graph.edge(f"q{state_map[start_state]}", f"q{state_map[next_state]}", label='ε')
                graph.edge(f"q{state_map[next_state]}", f"q{state_map[final_state]}", label='ε')
                print(f"{sub_component} - зацикливание в состоянии и e-переход перед этим состоянием")
            elif operator == '+':
                graph.edge(f"q{state_map[next_state]}", f"q{state_map[next_state]}", label=sub_component)
                graph.edge(f"q{state_map[next_state]}", f"q{state_map[final_state]}", label='ε')
                print(f"{sub_component} - зацикливание в состоянии и один обязательный переход перед этим состоянием")
    else:
        if component.startswith('(') and component.endswith(')'):
            sub_components = split_regex(component[1:-1])
            for sub_component in sub_components:
                next_state = f"q{len(state_map)}"
                state_map[next_state] = len(state_map)
                graph.edge(f"q{state_map[start_state]}", f"q{state_map[next_state]}", label=sub_component)
                process_component(sub_component, graph, next_state, final_state, state_map)
        else:
            sub_components = split_regex(component)
            for sub_component in sub_components:
                if '(' in sub_component and ')' in sub_component:
                    if not (sub_component.startswith('(') and sub_component.endswith(')')):
                        print(f"{sub_component} - разбитие на подкомпоненты")
                        # Разбиваем подкомпонент на элемент, обернутый в скобки, и остаток
                        open_index = sub_component.find('(')
                        close_index = sub_component.rfind(')')
                        if open_index != -1 and close_index != -1:
                            wrapped_component = sub_component[open_index:close_index+1]
                            remaining_component = sub_component[:open_index] + sub_component[close_index+1:]
                            process_component(wrapped_component, graph, start_state, final_state, state_map)
                            process_component(remaining_component, graph, start_state, final_state, state_map)
                        else:
                            process_component(sub_component, graph, start_state, final_state, state_map)
                else:
                    next_state = f"q{len(state_map)}"
                    state_map[next_state] = len(state_map)
                    graph.edge(f"q{state_map[start_state]}", f"q{state_map[next_state]}", label=sub_component)
                    graph.edge(f"q{state_map[next_state]}", f"q{state_map[final_state]}", label='ε')
                    print(sub_component)

def main():
    regex = "(abc)*(ab)*"
    components = split_regex(regex)
    graph = Digraph()

    start_state = "q0"
    final_state = "qF"
    state_map = {start_state: 0, final_state: 1}
    graph.node(f"q{state_map[start_state]}", shape="circle")
    graph.node(f"q{state_map[final_state]}", shape="doublecircle")

    for component in components:
        next_state = f"q{len(state_map)}"
        state_map[next_state] = len(state_map)
        graph.edge(f"q{state_map[start_state]}", f"q{state_map[next_state]}", label='ε')
        graph.edge(f"q{state_map[next_state]}", f"q{state_map[final_state]}", label='ε')
        process_component(component, graph, next_state, final_state, state_map)

    graph.render('regex_graph', format='png', view=True)

if __name__ == "__main__":
    main()