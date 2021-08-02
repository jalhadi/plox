from token import Token
from tokenType import TokenType

keywords = {
    'and': TokenType.AND,
    'class': TokenType.CLASS,
    'else': TokenType.ELSE,
    'false': TokenType.FALSE,
    'for': TokenType.FOR,
    'fun': TokenType.FUN,
    'if': TokenType.IF,
    'nil': TokenType.NIL,
    'or': TokenType.OR,
    'print': TokenType.PRINT,
    'return': TokenType.RETURN,
    'super': TokenType.SUPER,
    'this': TokenType.THIS,
    'true': TokenType.TRUE,
    'var': TokenType.VAR,
    'while': TokenType.WHILE,
}

class Scanner:
    def __init__(self, source):
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens = []
        self.source = source

    def scanTokens(self):        
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        self.tokens.append(Token(TokenType.EOF, '', None, self.line))
        return self.tokens

    def scanToken(self):
        c = self.advance()
        if c == '(': self.addToken(TokenType.LEFT_PAREN)
        elif c == ')': self.addToken(TokenType.RIGHT_PAREN)
        elif c == '{': self.addToken(TokenType.LEFT_BRACE)
        elif c == '}': self.addToken(TokenType.RIGHT_BRACE)
        elif c == ',': self.addToken(TokenType.COMMA)
        elif c == '.': self.addToken(TokenType.DOT)
        elif c == '-': self.addToken(TokenType.MINUS)
        elif c == '+': self.addToken(TokenType.PLUS)
        elif c == ';': self.addToken(TokenType.SEMICOLON)
        elif c == '*': self.addToken(TokenType.STAR)
        elif c == '!': self.addToken(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG);
        elif c == '=': self.addToken(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL);
        elif c == '<': self.addToken(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS);
        elif c == '>': self.addToken(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER);
        elif c == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.isAtEnd():
                    self.advance()
            else:
                self.addToken(TokenType.SLASH)
        elif any([c == x for x in [' ', '\r', '\t']]):
            pass
        elif c == '\n':
            self.line += 1
        elif c == '"':
            self.string()
        else:
            if self.isDigit(c):
                self.number()
            elif self.isAlpha(c):
                self.identifier()
            else:
                Lox.error(self.line, 'Unexpected character.')

    def match(self, expected):
        if self.isAtEnd(): return False
        if self.source[self.current] != expected: return False

        self.current += 1
        return True

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        return c

    def addToken(self, tokenType, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(tokenType, text, literal, self.line))

    def number(self):
        while self.isDigit(self.peek()):
            self.advance()

        if self.peek() == '.' and self.isDigit(self.peekNext()):
            self.advance()
            while self.isDigit(self.peek()):
                self.advance()

        self.addToken(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def string(self):
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.isAtEnd():
            Lox.error(self.line, 'Unterminated string.')
            return

        self.advance()
        value = self.source(self.start + 1, self.current - 1)
        self.addToken(TokenType.STRING, value)

    def identifier(self):
        while self.isAlphaNumeric(self.peek()):
            self.advance()
        text = self.source[self.start:self.current]
        if text in keywords:
            tokenType = keywords[text]
        else:
            tokenType = TokenType.IDENTIFIER
        self.addToken(tokenType)

    def isAlphaNumeric(self, c):
        return self.isAlpha(c) or self.isDigit(c)

    def isAlpha(self, c):
        return (c >= 'a' and c <= 'z') or \
            (c >= 'A' and c <= 'Z') or \
            c == '_'

    def isDigit(self, c):
        return c >= '0' and c <= '9'

    def peek(self):
        if self.isAtEnd():
            return '\0'
        return self.source[self.current]

    def peekNext(self):
        if self.current + 1 >= len(self.source): return '\0'
        return self.source[self.current + 1]

    def isAtEnd(self):
        return self.current >= len(self.source)