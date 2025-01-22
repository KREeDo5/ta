def valid_brackets(reg, firstIteration):
    opened_brackets = 0
    for i in reg:
        if i == '(':
            opened_brackets += 1
        if i == ')':
            opened_brackets -= 1
        if opened_brackets < 0:
            if firstIteration:
                print('Пропущены закрывающие скобки!')
            return False
    if opened_brackets == 0:
        return True
    if firstIteration:
        print('Пропущены открывающие скобки !')
    return False