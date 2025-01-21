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

def process_component(component):
    if component.endswith('*') or component.endswith('+'):
        operator = component[-1]
        sub_component = component[:-1]
        if sub_component.startswith('(') and sub_component.endswith(')'):
            sub_components = split_regex(sub_component[1:-1])
            for sub_component in sub_components:
                if operator == '*':
                    print(f"{sub_component} - зацикливание в состоянии и e-переход перед этим состоянием")
                elif operator == '+':
                    print(f"{sub_component} - зацикливание в состоянии и один обязательный переход перед этим состоянием")
        else:
            if operator == '*':
                print(f"{sub_component} - зацикливание в состоянии и e-переход перед этим состоянием")
            elif operator == '+':
                print(f"{sub_component} - зацикливание в состоянии и один обязательный переход перед этим состоянием")
    else:
        if component.startswith('(') and component.endswith(')'):
            sub_components = split_regex(component[1:-1])
            for sub_component in sub_components:
                process_component(sub_component)
        else:
            sub_components = split_regex(component)
            for sub_component in sub_components:
                print(sub_component)

def main():
    regex = "xy*(x|y*)|(ab(x|y*)*)|((x|a*)(x|y*))+"
    components = split_regex(regex)
    for component in components:
        process_component(component)

if __name__ == "__main__":
    main()