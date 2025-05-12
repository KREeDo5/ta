import sys
from typing import List, Dict, Optional, Set, Tuple

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

class Rule:
    def __init__(self, name: str, patterns: List[str]):
        self.name = name
        self.patterns = [p.split() for p in patterns]

class RuleSet:
    def __init__(self, title: str, rules: Set[Rule]):
        self.title = title
        self.rules = {r.name: r for r in rules}

class RuleEngine:
    """Движок обработки правил"""
    def __init__(self):
        self.rule_sets = [
            RuleSet(
                "Первый набор правил",
                {
                    Rule("A1", ["A1 ay A2", "A2"]),
                    Rule("A2", ["A2 ку A3", "A3"]),
                    Rule("A3", ["ух-ты", "хо A3", "ну A1 и_ну"])
                }
            ),
            RuleSet(
                "Второй набор правил",
                {
                    Rule("ПР1", ["ой ПР2 ай ПР3"]),
                    Rule("ПР2", ["ну", "ну ПР2"]),
                    Rule("ПР3", ["хо ПР3 хо", "ух-ты"])
                }
            )
        ]
        self.all_rules = {}
        for rs in self.rule_sets:
            self.all_rules.update(rs.rules)

    def analyze(self, text: str) -> Tuple[Optional[RuleSet], Optional[Rule]]:
        """Анализ текста с возвратом первого подходящего набора"""
        state = TextState(text)

        for rule_set in self.rule_sets:
            first_rule = next(iter(rule_set.rules.values()), None)
            if first_rule and self._try_rule(first_rule, state) and state.at_end():
                return rule_set, first_rule

        return None, None

    def _try_rule(self, rule: Rule, state: TextState) -> bool:
        """Попытка применить правило с отслеживанием пути"""
        if rule.name in state.rule_path:  # Защита от циклической рекурсии
            print(f"{rule.name} в {state.rule_path}")
            return False
        state.rule_path.append(rule.name)
        for pattern in rule.patterns:
            saved = state.save()
            if self._try_pattern(pattern, state):
                return True
            state.restore(saved)
        state.rule_path.pop()
        return False

    def _try_pattern(self, pattern: List[str], state: TextState) -> bool:
        """Попытка применить шаблон правила"""
        for token in pattern:
            if token in self.all_rules:
                if not self._try_rule(self.all_rules[token], state):
                    return False
            else:
                if not state.consume(token):
                    return False
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