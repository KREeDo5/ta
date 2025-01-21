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

def main():
    regex = "x|y*(x|y*)+|ab(x|y*)|(x|a*)(x|y*)"
    components = split_regex(regex)
    for component in components:
        print(component)

if __name__ == "__main__":
    main()