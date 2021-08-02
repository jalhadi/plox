class Token:
    def __init__(self, tokenType, lexeme, literal, line):
        self.type = tokenType
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def toString(self):
        return '{} {} {}'.format(self.type, self.lexeme, self.literal)
