# renamed the file from token.py to token_2.py
# as token results in a conflict with some
# other file named token.py in the python language
class Token:
    def __init__(self, tokenType, lexeme, literal, line):
        self.type = tokenType
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def toString(self):
        return '{} {} {}'.format(self.type, self.lexeme, self.literal)
