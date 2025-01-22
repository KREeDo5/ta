from copy import deepcopy
from validator import valid_brackets

empty_transit = 'ε'

class GraphNode:
    @staticmethod
    def remove_brackets(regex):
        while regex[0] == '(' and regex[-1] == ')' and valid_brackets(regex[1:-1], False):
            regex = regex[1:-1]
        return regex

    @staticmethod
    def is_concat(symb, alphabet):
        return symb == '(' or GraphNode.is_letter(symb, alphabet)

    @staticmethod
    def is_letter(symb, alphabet):
        return symb in alphabet

    def __init__(self, regex, alphabet):
        self.emptyTransit = None # eps-переход или нет
        self.item = None         # Символ или оператор
        self.position = None     # Позиция в регулярном выражении
        self.isSymbol = None     # Является ли точка символ - или это оператор
        self.child = []          # Дочерние узлы
        self.firstpos = []
        self.lastpos = []

        print('Current : ' + regex)

        self.isSymbol = (regex == '.') and ('.' in alphabet)

        # Конечный ли узел (вершина)
        if len(regex) == 1 and self.is_letter(regex, alphabet):
            self.item = regex # Найденный символ
            self.emptyTransit = (self.item == empty_transit)
            return

        # Узел не конечный (имеет операторы)
        operatorLoop = -1 # петля (звезда Клини)
        operatorPlus = -1
        operatorOR = -1
        operatorDot = -1  # конкатенация
        i = 0

        while i < len(regex):
            if regex[i] == '(':
                nesting = 1 # вложенность
                i += 1
                # пока не находим закрывающую скобку, пропускаем все символы
                while nesting != 0 and i < len(regex):
                    if regex[i] == '(':
                        nesting += 1
                    if regex[i] == ')':
                        nesting -= 1
                    i += 1
            else:
                i += 1

            if i == len(regex): # Выходим из цикла, если не разбили выражение в скобках
                break

            # оставшееся выражение без внешних скобок, ищем индексы операторов
            if self.is_concat(regex[i], alphabet):
                if operatorDot == -1:
                    operatorDot = i
                continue
            if regex[i] == '*':
                if operatorLoop == -1:
                    operatorLoop = i
                continue
            if regex[i] == '+':
                if operatorPlus == -1:
                    operatorPlus = i
                continue
            if regex[i] == '|':
                if operatorOR == -1:
                    operatorOR = i
                i += 1

        # Разбиваем выражение на части
        if operatorOR != -1:
            self.item = '|'
            self.child.append(GraphNode(self.remove_brackets(regex[:operatorOR]), alphabet))
            self.child.append(GraphNode(self.remove_brackets(regex[(operatorOR + 1):]), alphabet))
        elif operatorDot != -1:
            self.item = '.'
            self.child.append(GraphNode(self.remove_brackets(regex[:operatorDot]), alphabet))
            self.child.append(GraphNode(self.remove_brackets(regex[operatorDot:]), alphabet))
        elif operatorPlus != -1:
            self.item = '+'
            self.child.append(GraphNode(regex[:operatorPlus] + regex[:operatorPlus] + '*', alphabet))
        elif operatorLoop != -1:
            self.item = '*'
            self.child.append(GraphNode(self.remove_brackets(regex[:operatorLoop]), alphabet))

    def calc_functions(self, pos, followpos, alphabet):
        # Если это конечный узел (вершина)
        if self.isSymbol or (self.is_letter(self.item, alphabet) and self.item != '.'):
            self.firstpos = [pos]
            self.lastpos = [pos]
            self.position = pos
            # Добавляем текущий узел (позицию) в список followpos
            followpos.append([self.item, []])
            return pos + 1
        # Если это дочерний узел
        for child in self.child:
            pos = child.calc_functions(pos, followpos, alphabet)

        # обрабатываем действия операторов
        if self.item == '.':
            if self.child[0].emptyTransit:
                self.firstpos = sorted(list(set(self.child[0].firstpos + self.child[1].firstpos)))
            else:
                self.firstpos = deepcopy(self.child[0].firstpos)
            if self.child[1].emptyTransit:
                self.lastpos = sorted(list(set(self.child[0].lastpos + self.child[1].lastpos)))
            else:
                self.lastpos = deepcopy(self.child[1].lastpos)
            self.emptyTransit = self.child[0].emptyTransit and self.child[1].emptyTransit
            # обновляю Followpos для позиций в lastpos первого дочернего узла, добавляя firstpos второго дочернего узла
            for i in self.child[0].lastpos:
                for j in self.child[1].firstpos:
                    if j not in followpos[i][1]:
                        followpos[i][1] = sorted(followpos[i][1] + [j])

        elif self.item == '|':
            self.firstpos = sorted(list(set(self.child[0].firstpos + self.child[1].firstpos)))
            self.lastpos = sorted(list(set(self.child[0].lastpos + self.child[1].lastpos)))
            self.emptyTransit = self.child[0].emptyTransit or self.child[1].emptyTransit

        elif self.item == '*':
            self.firstpos = deepcopy(self.child[0].firstpos)
            self.lastpos = deepcopy(self.child[0].lastpos)
            self.emptyTransit = True
            # Followpos
            for i in self.child[0].lastpos:
                for j in self.child[0].firstpos:
                    if j not in followpos[i][1]:
                        followpos[i][1] = sorted(followpos[i][1] + [j])

        elif self.item == '+':
            self.firstpos = deepcopy(self.child[0].firstpos)
            self.lastpos = deepcopy(self.child[0].lastpos)
            self.emptyTransit = self.child[0].emptyTransit
            # Followpos
            for i in self.child[0].lastpos:
                for j in self.child[0].firstpos:
                    if j not in followpos[i][1]:
                        followpos[i][1] = sorted(followpos[i][1] + [j])

        return pos

    def write_level(self, level):
        print(str(level) + ' ' + self.item, self.firstpos, self.lastpos, self.emptyTransit,
              '' if self.position == None else self.position)
        for child in self.child:
            child.write_level(level + 1)