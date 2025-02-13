class Token(object):
    def __init__(self, type, token_name, item, line, start_pos, end_pos):
        self.type = type
        self.token_name = token_name
        self.item = item
        self.line = line
        self.start_pos = start_pos
        self.end_pos = end_pos

    def __str__(self):
        return f"{self.item} : {self.type}({self.token_name}) {self.line} : {self.start_pos}"
        #return f"{self.type}({self.token_name}) '{self.item}' at line {self.line}, pos {self.start_pos}-{self.end_pos}"