import sys
from typing import List, Dict, Optional

class Text:
    """Класс для работы с текстом и отслеживания позиции при анализе"""
    def __init__(self, text: str):
        self.text = text
        self.position = 0

    def get(self, index: int = 0) -> str:
        """Получить символ на текущей позиции + index"""
        if self.position + index >= len(self.text):
            return ''
        return self.text[self.position + index]

    def next(self, count: int = 1) -> None:
        """Переместить позицию вперед на count символов"""
        self.position += count

    def copy(self) -> 'Text':
        """Создать копию текста с текущей позиции"""
        return Text(self.text[self.position:])

    def remaining_text(self) -> str:
        """Получить оставшийся текст с текущей позиции"""
        return self.text[self.position:]

    def __str__(self) -> str:
        return self.text[self.position:]


class Rule:
    """Базовый класс для правил"""
    def __init__(self, name: str):
        self.name = name
        self.subrules = []

    def add_subrule(self, subrule: str) -> None:
        """Добавить подправило"""
        self.subrules.append(subrule)

    def match(self, text: Text) -> bool:
        """Попытаться применить правило к тексту"""
        raise NotImplementedError("Subclasses must implement this method")

    def __str__(self) -> str:
        return f"{self.name}: {', '.join(self.subrules)}"


class RuleParser:
    """Класс для парсинга правил из файлов"""
    @staticmethod
    def parse_rule_file(filename: str) -> Dict[str, Rule]:
        """Парсинг файла с правилами"""
        rules = {}
        current_rule = None

        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                if line.endswith(':'):
                    # Новая группа правил
                    rule_name = line[:-1].strip()
                    current_rule = Rule(rule_name)
                    rules[rule_name] = current_rule
                elif line.startswith('-'):
                    # Подправило
                    subrule = line[1:].strip()
                    if current_rule is not None:
                        current_rule.add_subrule(subrule)

        return rules


class TextAnalyzer:
    """Основной класс для анализа текста по правилам"""
    def __init__(self):
        self.rules = {}

    def load_rules(self, rule_files: List[str]) -> None:
        """Загрузка правил из файлов"""
        for rule_file in rule_files:
            file_rules = RuleParser.parse_rule_file(rule_file)
            self.rules.update(file_rules)

    def analyze_text(self, text: str) -> Optional[str]:
        """Анализ текста по загруженным правилам"""
        text_obj = Text(text)

        for rule_name, rule in self.rules.items():
            # Создаем копию текста для каждого правила
            temp_text = text_obj.copy()
            if self._try_rule(rule, temp_text):
                return rule_name

        return None

    def _try_rule(self, rule: Rule, text: Text) -> bool:
        """Попытка применить правило и его подправила к тексту"""
        for subrule in rule.subrules:
            # Создаем новую копию текста для каждого подправила
            temp_text = text.copy()
            if self._match_subrule(subrule, temp_text):
                # Если подправило сработало, обновляем позицию в основном тексте
                text.position = temp_text.position
                return True
        return False

    def _match_subrule(self, subrule: str, text: Text) -> bool:
        """Попытка сопоставить подправило с текстом"""
        tokens = subrule.split()
        i = 0
        n = len(tokens)

        while i < n and text.position < len(text.text):
            token = tokens[i]

            if token.startswith('(') and token.endswith(')'):
                # Это группа правил (рекурсивный вызов)
                group_name = token[1:-1]
                if group_name in self.rules:
                    if not self._try_rule(self.rules[group_name], text):
                        return False
                else:
                    return False
            else:
                # Это литерал (точное совпадение)
                if not self._match_literal(token, text):
                    return False

            i += 1

        return i == n

    def _match_literal(self, literal: str, text: Text) -> bool:
        """Попытка сопоставить литерал с текстом"""
        literal_len = len(literal)
        if text.position + literal_len > len(text.text):
            return False

        if text.text[text.position:text.position + literal_len] == literal:
            text.next(literal_len)
            return True
        return False


def main():
    if len(sys.argv) < 3:
        print("Использование: python analyzer.py input.txt rule1.txt rule2.txt ...")
        print("Или: analyzer.exe input.txt rule1.txt rule2.txt ...")
        return

    input_file = sys.argv[1]
    rule_files = sys.argv[2:]

    # Чтение входного текста
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            input_text = file.read().strip()
    except FileNotFoundError:
        print(f"Ошибка: входной файл '{input_file}' не найден")
        return

    # Инициализация и загрузка правил
    analyzer = TextAnalyzer()
    try:
        analyzer.load_rules(rule_files)
    except FileNotFoundError as e:
        print(f"Ошибка: файл правила '{e.filename}' не найден")
        return

    # Анализ текста
    matched_rule = analyzer.analyze_text(input_text)

    # Вывод результата
    if matched_rule:
        print(f'"{input_text}" - это говорит "{matched_rule}"')
    else:
        print(f'"{input_text}" - const ERROR')


if __name__ == "__main__":
    main()