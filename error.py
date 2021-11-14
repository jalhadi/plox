from tokenType import TokenType


class Error:
    hadError = False

    def error(line, message):
        Error.report(line, "", message)

    def tokenError(token, message):
        if token.type == TokenType.EOF:
            Error.report(token.line, " at end ", message)
        else:
            Error.report(token.line, " at '{}'".format(token.lexeme), message)

    def report(line, where, message):
        print("[{}] Error {}: {}".format(line, where, message))
        hadError = True
