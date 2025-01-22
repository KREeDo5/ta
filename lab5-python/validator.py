def valid_brackets(reg):
    opened_brackets = 0
    for i in reg:
        if i == '(':
            opened_brackets += 1
        if i == ')':
            opened_brackets -= 1
        if opened_brackets < 0:
            print('Пропущены закрывающие скобки!')
            return False
    if opened_brackets == 0:
        return True
    print('Пропущены открывающие скобки !')
    return False