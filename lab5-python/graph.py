from dfa import Dfa
from graph_node import GraphNode

empty_transit = 'ε'

class Graph:
    def __init__(self, regex, alphabet):
        self.root = GraphNode(regex, alphabet)
        self.followpos = []
        self.alphabet = alphabet
        self.functions()

    def functions(self):
        self.root.calc_functions(0, self.followpos, self.alphabet)
        # print(self.followpos)

    def toDfa(self, alphabet):

        def isFinal(q):
            for i in q:
                if self.followpos[i][0] == '#':
                    return True
            return False
        q0 = self.root.firstpos
        Alph = alphabet - {'#', empty_transit}

        SList = []        # Список состояний
        FList = []        # Финальные состояния
        CheckedList = []  # Обработанные состояния
        TransList = []    # Переходы, например: TransList[S] = {'a': S2, 'b': S0}

        SList.append(q0)
        if isFinal(q0):
            FList.append(SList.index(q0))

        while len(SList) - len(CheckedList) > 0: # Пока есть необработанные состояния
            TransList.append({})

            q = [i for i in SList if i not in CheckedList][0] # Берем первое необработанное состояние
            CheckedList.append(q)

            for a in Alph:
                Transition = []
                # Нахожу новое состояние из необработанного - объединение всех переходов по символу a
                for i in q:
                    if self.followpos[i][0] == a:
                        Transition = Transition + self.followpos[i][1]
                # Убираю дубликаты и сортирую
                Transition = sorted(list(set(Transition)))

                # Если множество пустое - пропускаю, не добавляю в список состояний
                if len(Transition) == 0:
                    continue

                if Transition not in SList:
                    SList.append(Transition)
                    # Помечаю что состояние - финальное
                    if isFinal(Transition):
                        FList.append(SList.index(Transition))
                # Добавляю переход для необработанного состояния по символу a
                # Указываю, что переход ведет в состояние Transition
                TransList[SList.index(q)][a] = SList.index(Transition)

        return Dfa(SList, Alph, TransList, SList.index(q0), FList)