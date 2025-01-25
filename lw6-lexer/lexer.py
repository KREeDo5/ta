from lexer_token import Token
import re

#TODO:
# обработка чисел. Если после корректного числа идёт любой другой символ - ошбибка
# обработка ковычек

class Lexer(object):
    def __init__(self):
        """ Инициализация лексера с правилами.
        :param rules: Список правил [(regex, token_name, type)].
        # :param skip_whitespace: Пропускать ли пробелы.
        """
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

        # # Пропускаем пробелы, если это включено
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

        # Проверка на открывающий символ /* без закрывающего */
        if self.text[self.pos:].startswith('/*'):
            end_comment = self.text.find('*/', self.pos)
            if end_comment == -1:  # Если закрывающий символ не найден
                start_pos = self.pos
                value = self.text[self.pos:self.pos + 2]  # Берем только /* для ошибки
                token = Token(
                    type="error",
                    token_name="unterminated_comment",
                    item=value,
                    line=self.line,
                    start_pos=start_pos - self.line_start,
                    end_pos=self.pos + 2 - self.line_start,
                )
                self.pos += 2  # Продолжаем анализ с символа после /*
                return token

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


class LexerError(Exception):
    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return f"Lexer error at position {self.pos}"

# Правила лексера
rules = [
    # Комментарии
    (r'//.*', 'single_line_comment', 'comment'),
    (r'/\*[\s\S]*?\*/', 'multi_line_comment', 'comment'),

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

    # Идентификаторы
    (r'_[a-zA-Zа-яА-ЯёЁ0-9][_a-zA-Zа-яА-ЯёЁ0-9]*', 'private_id', 'identifier'),
    (r'[a-zA-Zа-яА-ЯёЁ][_a-zA-Zа-яА-ЯёЁ0-9]*', 'public_id', 'identifier'),

    # Числа
    (r'0b[01]+', 'binary', 'number'),                       # Двоичные числа (0b101)
    (r'0o[0-7]+', 'octal', 'number'),                       # Восьмеричные числа (0o71)
    (r'0x[\da-fA-F]+', 'hex', 'number'),                    # Шестнадцатеричные числа (0x1A45F0D)
    (r'\d+\.\d+e[+-]?\d+', 'scientific_float', 'number'),   # Числа в научной нотации с точкой (123.456e+8)
    (r'\d+\.\d+', 'float', 'number'),                       # Числа с плавающей точкой (123.456)
    (r'\d+e[+-]?\d+', 'scientific', 'number'),              # Числа в научной нотации (1e-8)
    (r'\d+', 'integer', 'number'),                          # Десятичные целые числа (123)

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

    # Скобки
    (r'\(', 'bracket_open', 'bracket'),
    (r'\)', 'bracket_close', 'bracket'),
    (r'\{', 'brace_open', 'bracket'),
    (r'\}', 'brace_close', 'bracket'),
    (r'\[', 'bracket_sq_open', 'bracket'),
    (r'\]', 'bracket_sq_close', 'bracket'),
]
