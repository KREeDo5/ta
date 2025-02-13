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

# Правила лексера
rules = [
    # Комментарии
    (r'//.*', 'single_line_comment', 'comment'),
    (r'/\*[\s\S]*?\*/', 'multi_line_comment', 'comment'),

    (r'/\*', 'unterminated_comment', 'error'),

    # Строковые литералы
    # (r'"(?:[^"\\]|\\.)*"', 'double_quoted_string', 'string_literal'),
    # (r"'(?:[^'\\]|\\.)*'", 'single_quoted_string', 'string_literal'),

    (r'"', 'double_quote', 'quote'),
    (r"'", 'single_quote', 'quote'),

    # (r'"', 'unterminated_double_quote', 'error'),
    # (r"'", 'unterminated_single_quote', 'error'),

    # (r'\((?:[^"\\]|\\.)*"', 'unterminated_bracket_open', 'error'),
    # (r"\{(?:[^'\\]|\\.)*'", 'unterminated_brace_open', 'error'),
    # (r"\[(?:[^'\\]|\\.)*'", 'unterminated_bracket_sq_open', 'error'),

    # Скобки
    (r'\(', 'bracket_open', 'bracket'),
    (r'\)', 'bracket_close', 'bracket'),
    (r'\{', 'brace_open', 'bracket'),
    (r'\}', 'brace_close', 'bracket'),
    (r'\[', 'bracket_sq_open', 'bracket'),
    (r'\]', 'bracket_sq_close', 'bracket'),

    # Условные конструкции
    (r'\bint\b', 'int', 'keyword'),
    (r'\bdouble\b', 'double', 'keyword'),
    (r'\bchar\b', 'char', 'keyword'),
    (r'\bstring\b', 'string', 'keyword'),
    (r'\bbool\b', 'bool', 'keyword'),
    (r'\bif\b', 'if', 'keyword'),
    (r'\bwhile\b', 'while', 'keyword'),
    (r'\bfor\b', 'for', 'keyword'),
    (r'\btrue\b', 'true', 'keyword'),
    (r'\bfalse\b', 'false', 'keyword'),

    # Длинные ошибочные идентификаторы (30 >=)
    (r'_*[_a-zA-Zа-яА-ЯёЁ0-9][\.]*{29,}', 'overflow_id', 'error'),

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
    (r';', 'semicolon', 'separator'),
    (r',', 'comma', 'separator'),
    (r'/n', 'newline', 'separator'),
    (r'/t', 'tab', 'separator'),

    # Операторы
    (r'\+', 'plus', 'operator'),
    (r'-', 'minus', 'operator'),
    (r'\*', 'multiply', 'operator'),
    (r'/', 'divide', 'operator'),
    (r'%', 'module', 'operator'),
    (r'!=', 'not_equal', 'operator'),
    (r'===', 'strict_equal', 'operator'),
    (r'==', 'equal', 'operator'),
    (r'=', 'set', 'operator'),
    (r'<=', 'less_equal', 'operator'),
    (r'>=', 'greater_equal', 'operator'),
    (r'<', 'less', 'operator'),
    (r'>', 'greater', 'operator'),
]
