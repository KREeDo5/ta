from lexer_token import Token
import re

class Lexer(object):
    def __init__(self):
        self.group_type = {}
        self.regex_parts = []

        # Создание группированных правил
        for idx, (regex, token_name, token_type) in enumerate(rules, start=1):
            group_name = f'GROUP{idx}'
            self.regex_parts.append(f"(?P<{group_name}>{regex})")
            self.group_type[group_name] = (token_name, token_type)

        self.regex = re.compile('|'.join(self.regex_parts), re.VERBOSE)
        self.text = None
        self.pos = 0
        self.line = 1
        self.line_start = 0

    def input(self, text):
        """ Устанавливает текст для анализа. """
        self.text = text
        self.pos = 0
        self.line = 1
        self.line_start = 0

    def token(self):
        """ Возвращает следующий токен. """
        if self.pos >= len(self.text):
            return None

        # if self.skip_whitespace:
        whitespace_match = re.match(r'\s+', self.text[self.pos:])
        if whitespace_match:
            whitespace = whitespace_match.group(0)
            self.pos += whitespace_match.end()
            newline_count = whitespace.count('\n')
            if newline_count > 0:
                self.line += newline_count
                self.line_start = self.pos - len(whitespace.split('\n')[-1])

        if self.pos >= len(self.text):
            return None

        # Ищем соответствие
        match = self.regex.match(self.text, self.pos)
        if match:
            group_name = match.lastgroup
            token_name, token_type = self.group_type[group_name]
            start_pos = self.pos
            end_pos = match.end()
            value = match.group(group_name)

            # Создаем токен
            token = Token(
                type=token_type,
                token_name=token_name,
                item=value,
                line=self.line,
                start_pos=start_pos - self.line_start,
                end_pos=end_pos - self.line_start,
            )

            # Обновляем текущую позицию
            self.pos = end_pos
            self.line += value.count('\n')
            if '\n' in value:
                self.line_start = self.pos - len(value.split('\n')[-1])
            return token

        # Если ни одно правило не совпало, возвращаем ошибочный токен
        error_value = self.text[self.pos]
        token = Token(
            type="error",
            token_name="unknown",
            item=error_value,
            line=self.line,
            start_pos=self.pos - self.line_start,
            end_pos=self.pos + 1 - self.line_start,
        )
        self.pos += 1
        return token

    def tokens(self):
        """ Генератор токенов. """
        while True:
            token = self.token()
            if token is None:
                break
            yield token
        yield Token(
            type="separator",
            token_name="end",
            item="",
            line=self.line,
            start_pos=self.pos - self.line_start,
            end_pos=self.pos - self.line_start,
        )

# Правила лексера
rules = [
    # Комментарии
    (r'//.*', 'single_line_comment', 'comment'),
    (r'/\*[\s\S]*?\*/', 'multi_line_comment', 'comment'),
    # Незавершённый многострочный комментарий
    (r'/\*', 'unterminated_comment', 'error'),

    # Символьные литералы (char)
    (r'"(?:.|\\.)"', 'double_quoted_char', 'char_literal'),                   # Символьный литерал в двойных кавычках
    (r"'(?:.|\\.)'", 'single_quoted_char', 'char_literal'),                   # Символьный литерал в одинарных кавычках

    # Строковые литералы
    (r'"(?:[^"\\]|\\.)*"', 'double_quoted_string', 'string_literal'),         # Строка в двойных кавычках
    (r"'(?:[^'\\]|\\.)*'", 'single_quoted_string', 'string_literal'),         # Строка в одинарных кавычках

    # (r'"', 'double_quote', 'quote'),
    # (r"'", 'single_quote', 'quote'),

    # Незакрытые кавычки и скобки
    (r'"', 'unterminated_double_quote', 'error'),
    (r"'", 'unterminated_single_quote', 'error'),
    (r'\((?:[^"\\]|\\.)*"$', 'unterminated_bracket_open', 'error'),
    (r'\{(?:[^\'\\]|\\.)*\'$', 'unterminated_brace_open', 'error'),
    (r'\[(?:[^\'\\]|\\.)*\'$', 'unterminated_bracket_sq_open', 'error'),

    # Скобки
    (r'\(', 'bracket_open', 'bracket'),                                       # Открывающая круглая скобка (
    (r'\)', 'bracket_close', 'bracket'),                                      # Закрывающая круглая скобка )
    (r'\{', 'brace_open', 'bracket'),                                         # Открывающая фигурная скобка {
    (r'\}', 'brace_close', 'bracket'),                                        # Закрывающая фигурная скобка }
    (r'\[', 'bracket_sq_open', 'bracket'),                                    # Открывающая квадратная скобка [
    (r'\]', 'bracket_sq_close', 'bracket'),                                   # Закрывающая квадратная скобка ]

    # Ключевые слова
    (r'\bint\b', 'int', 'keyword'),                                           # Целочисленный тип (int)
    (r'\bdouble\b', 'double', 'keyword'),                                     # Число с плавающей точкой (double)
    (r'\bchar\b', 'char', 'keyword'),                                         # Символьный тип (char)
    (r'\bstring\b', 'string', 'keyword'),                                     # Строковый тип (string)
    (r'\bbool\b', 'bool', 'keyword'),                                         # Логический тип (bool)
    (r'\bif\b', 'if', 'keyword'),                                             # Условный оператор (if)
    (r'\belse\b', 'else', 'keyword'),                                         # Альтернативный условный оператор (else)
    (r'\bwhile\b', 'while', 'keyword'),                                       # Цикл while (while)
    (r'\bfor\b', 'for', 'keyword'),                                           # Цикл for (for)
    (r'\btrue\b', 'true', 'keyword'),                                         # Логическое значение true (true)
    (r'\bfalse\b', 'false', 'keyword'),                                       # Логическое значение false (false)

    # Длинные ошибочные идентификаторы (30 >=)
    (r'_?[_a-zA-Zа-яА-ЯёЁ0-9\.]{30,}', 'overflow_id', 'error'),

    # Идентификаторы (длина 1-30)
    (r'_[a-zA-Zа-яА-ЯёЁ0-9][_a-zA-Zа-яА-ЯёЁ0-9]{0,28}', 'private_id', 'identifier'),
    (r'[a-zA-Zа-яА-ЯёЁ][_a-zA-Zа-яА-ЯёЁ0-9]{0,28}', 'public_id', 'identifier'),

    # (r'_[а-яА-ЯёЁ0-9][_а-яА-ЯёЁ0-9]*', 'private_id_ru', 'identifier'),
    # (r'[а-яА-ЯёЁ][_а-яА-ЯёЁ0-9]*', 'public_id_ru', 'identifier'),
    # (r'_[a-zA-Z0-9][_a-zA-Z0-9]*', 'private_id_en', 'identifier'),
    # (r'[a-zA-Z][_a-zA-Z0-9]*', 'public_id_en', 'identifier'),

    # Неправильные форматы чисел
    (r'0[bB][^01\s]+', 'invalid_binary', 'error'),                            # Некорректные двоичные числа
    (r'0[oO][^0-7\s]+', 'invalid_octal', 'error'),                            # Некорректные восьмеричные числа
    (r'0[xX]([g-zG-Z]+|[\d]*[g-zG-Z]+[\d]*)', 'invalid_hex', 'error'),        # Некорректные шестнадцатеричные числа (0x1A45F0D)
    (r'0[^bBoOxX0-9][\da-zA-Z]+', 'unsupported_number_system', 'error'),      # Неподдерживаемая система счисления
    (r'(\d+\.\d+[\.]+[\d]*)', 'invalid_float', 'error'),                      # Лишние точки в числе
    (r'\d+e[+-]?\d+\.\d+', 'invalid_scientific', 'error'),                    # Неверная научная нотация
    (r'\.\d+', 'invalid_leading_dot', 'error'),                               # Начало с точки без целой части

    # Числа
    (r'0[bB][01]+', 'binary', 'number'),                                      # Двоичные числа (0b101)
    (r'0[oO][0-7]+', 'octal', 'number'),                                      # Восьмеричные числа (0o71)
    (r'0[xX][\da-fA-F]+', 'hex', 'number'),                                   # Шестнадцатеричные числа (0x1A45F0D)
    (r'\d+\.\d+e[+-]?\d+', 'scientific_float', 'number'),                     # Числа в научной нотации с точкой (123.456e+8)
    (r'\d+\.\d+', 'float', 'number'),                                         # Числа с плавающей точкой (123.456)
    (r'\d+e[+-]?\d+', 'scientific', 'number'),                                # Числа в научной нотации (1e-8)
    (r'\d+', 'integer', 'number'),                                            # Десятичные целые числа (123)

    (r'0[bB]$', 'unterminated_binary', 'error'),                              # Незавершённый префикс двоичных чисел
    (r'0[oO]$', 'unterminated_octal', 'error'),                               # Незавершённый префикс восьмеричных чисел
    (r'0[xX]$', 'unterminated_hex', 'error'),                                 # Незавершённый префикс шестнадцатеричных чисел

    # Разделители
    (r';', 'semicolon', 'separator'),                                         # Точка с запятой (;)
    (r',', 'comma', 'separator'),                                             # Запятая (,)
    (r'/n', 'newline', 'separator'),                                          # Новая строка (\n)
    (r'/t', 'tab', 'separator'),                                              # Табуляция

    # Операторы
    (r'\+', 'plus', 'operator'),                                              # Сложение (+)
    (r'-', 'minus', 'operator'),                                              # Вычитание (-)
    (r'\*', 'multiply', 'operator'),                                          # Умножение (*)
    (r'/', 'divide', 'operator'),                                             # Деление (/)
    (r'%', 'module', 'operator'),                                             # Остаток от деления (%)
    (r'!=', 'not_equal', 'operator'),                                         # Неравенство (!=)
    (r'===', 'strict_equal', 'operator'),                                     # Строгое равенство (===)
    (r'==', 'equal', 'operator'),                                             # Равенство (==)
    (r'=', 'set', 'operator'),                                                # Присваивание (=)
    (r'<=', 'less_equal', 'operator'),                                        # Меньше или равно (<=)
    (r'>=', 'greater_equal', 'operator'),                                     # Больше или равно (>=)
    (r'<', 'less', 'operator'),                                               # Меньше (<)
    (r'>', 'greater', 'operator'),                                            # Больше (>)
    (r'&&', 'and', 'operator'),                                               # Логическое И (&&)
    (r'\|\|', 'or', 'operator'),                                              # Логическое ИЛИ (||)
]
