import sys
from error import Error
from ast_printer import AstPrinter
from scanner import Scanner
from parser import Parser
from interpreter import Interpreter


class Lox:
    def __init__(self):
        self.interpreter = Interpreter()
        if sys.version_info[0] < 3:
            raise Exception("Python 3 or a more recent version is required.")
        if len(sys.argv) > 2:
            print("Usage: python3 plox.py [script]")
            sys.exit(64)
        elif len(sys.argv) > 1:
            self.runFile(sys.argv[0])
        else:
            self.runPrompt()

    def run(self, line):
        scanner = Scanner(line)
        tokens = scanner.scanTokens()
        parser = Parser(tokens)
        expression = parser.parse()
        if Error.hadError:
            return
        # Implement AstPrinter
        self.interpreter.interpret(expression)

    def runFile(self, filePath):
        with open(filePath) as f:
            read_data = f.read()
            self.run(read_data)
            if Error.hadError:
                sys.exit(65)
            if Error.hadRuntimeError:
                sys.exit(70)

    def runPrompt(self):
        while True:
            line = input("plox > ")
            if line == "":
                break
            self.run(line)
            # If there was an error in an interactive session
            # reset the error and don't kill the whole session
            # hadError = False
            Error.hadError = False


if __name__ == "__main__":
    lox = Lox()
