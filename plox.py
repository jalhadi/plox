import sys
from scanner import Scanner
from parser import Parser


class Lox:
    hadError = False
    def __init__(self):
        # self.hadError = False
        if sys.version_info[0] < 3:
            raise Exception("Python 3 or a more recent version is required.")
        if len(sys.argv) > 2:
            print('Usage: python3 plox.py [script]')
            sys.exit(64)
        elif len(sys.argv) > 1:
            self.runFile(sys.argv[0])
        else:
            self.runPrompt(); 

    def run(self, line):
        scanner = Scanner(line)
        tokens = scanner.scanTokens()
        parser = Parser(tokens)
        expression = parser.parse()
        if hadError:
            return
        # Implement AstPrinter

    def runFile(self, filePath):
        with open(filePath) as f:
            read_data = f.read()
            self.run(read_data)
            if hadError:
                sys.exit(65)

    def runPrompt(self):
        while True:
            line = input('plox > ')
            if line == '':
                break;
            self.run(line)
            # If there was an error in an interactive session
            # reset the error and don't kill the whole session
            hadError = False

    def error(self, line, message):
        self.report(line, '', message)

    def tokenError(self, token, message):
        if token.type == TokenType.EOF:
            self.report(token.line, " at end ", message)
        else:
            self.report(token.line, f" at '{token.lexeme}'", message)

    def report(self, line, where, message):
        print('[{}] Error {}: {}'.format(line, where, message))
        hadError = True

if __name__ == '__main__':
    lox = Lox()   
