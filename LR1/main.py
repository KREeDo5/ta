import sys
from typing import List, Dict, Optional, Tuple, OrderedDict

class TextState:
    """Состояние анализа текста с возможностью возврата"""
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.rule_path = []  # История примененных правил

    def save(self) -> Dict:
        """Сохранение текущего состояния"""
        return {'pos': self.pos, 'path': list(self.rule_path)}

    def restore(self, state: Dict):
        """Восстановление состояния"""
        self.pos = state['pos']
        self.rule_path = list(state['path'])

    def consume(self, token: str) -> bool:
        """Попытка потребить токен"""
        if self.text.startswith(token, self.pos):
            self.pos += len(token)
            return True
        return False

    def at_end(self) -> bool:
        """Проверка конца текста"""
        return self.pos >= len(self.text)

    def remaining(self) -> str:
        """Возвращает оставшуюся часть текста"""
        return self.text[self.pos:]

class Rule:
    """Отдельное правило с вариантами"""
    def __init__(self, name: str, patterns: List[str]):
        self.name = name
        self.patterns = [p.split() for p in patterns]

    def __repr__(self):
        return f"Rule(name={self.name}, patterns={self.patterns})"

class RuleSet:
    """Набор правил с заголовком"""
    def __init__(self, title: str, rules: List[Tuple[str, List[str]]]):
        self.title = title
        # Используем OrderedDict для сохранения порядка
        self.rules = OrderedDict()
        for name, patterns in rules:
            self.rules[name] = Rule(name, patterns)

    def __repr__(self):
        return f"RuleSet(title={self.title}, rules={list(self.rules.values())})"

class RuleEngine:
    """Движок обработки правил"""
    def __init__(self):
        # Жестко заданные правила с сохранением порядка
        self.rule_sets = [
            RuleSet(
                "Первый набор правил",
                [
                    ("A1", ["A1 ay A2", "A2"]),
                    ("A2", ["A2 ку A3", "A3"]),
                    ("A3", ["ух-ты", "хо A3", "ну A1 и_ну"])
                ]
            ),
            RuleSet(
                "Второй набор правил",
                [
                    ("ПР1", ["ой ПР2 ай ПР3"]),
                    ("ПР2", ["ну", "ну ПР2"]),
                    ("ПР3", ["хо ПР3 хо", "ух-ты"])
                ]
            )
        ]
        self.all_rules = {}
        for rs in self.rule_sets:
            self.all_rules.update(rs.rules)

    def analyze(self, text: str) -> Tuple[Optional[RuleSet], Optional[Rule]]:
        """Анализ текста с возвратом первого подходящего набора"""
        state = TextState(text)

        for rule_set in self.rule_sets:
            print(f"\nАнализируем набор правил: {rule_set.title}")
            # Берем первое правило в порядке объявления
            first_rule_name = next(iter(rule_set.rules.keys()))
            first_rule = rule_set.rules[first_rule_name]

            print(f"Пробуем начать с правила: {first_rule_name}")
            if self._try_rule(first_rule, state) and state.at_end():
                return rule_set, first_rule

            # Сбрасываем состояние для следующего набора правил
            state = TextState(text)

        return None, None

    def _try_rule(self, rule: Rule, state: TextState) -> bool:
        """Попытка применить правило с отслеживанием пути"""
        if rule.name in state.rule_path:  # Защита от циклической рекурсии
            print(f"Обнаружена циклическая рекурсия для правила {rule.name}")
            return False

        state.rule_path.append(rule.name)
        print(f"Входим в правило {rule.name}, текущий путь: {state.rule_path}")

        for pattern in rule.patterns:
            saved = state.save()
            print(f"Пробуем шаблон: {' '.join(pattern)}")
            if self._try_pattern(pattern, state):
                print(f"Шаблон {' '.join(pattern)} успешно применен")
                return True
            state.restore(saved)
            print(f"Откат состояния, позиция: {state.pos}")

        state.rule_path.pop()
        return False

    def _try_pattern(self, pattern: List[str], state: TextState) -> bool:
        saved = state.save()

        for token in pattern:
            if token in self.all_rules:
                if not self._try_rule(self.all_rules[token], state):
                    state.restore(saved)
                    return False
            else:
                if not state.consume(token):
                    state.restore(saved)
                    return False
                print(f"Успешно потребили '{token}', остаток: '{state.remaining()}'")

        return True

def main():
    input_file = r"D:\Repos\Github\tyap\LR1\dist\monkey0.txt"

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
    except FileNotFoundError:
        print(f"Ошибка: файл не найден")
        return

    engine = RuleEngine()
    rule_set, matched_rule = engine.analyze(text)

    if rule_set:
        print(f'"{text}" - это говорит "{rule_set.title}"')
    else:
        print(f'"{text}" - не соответствует ни одному набору правил')

if __name__ == "__main__":
    main()