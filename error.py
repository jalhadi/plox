from token_type import TokenType


class Error:
    hadError = False
    hadRuntimeError = False

    def error(line, message):
        Error.report(line, "", message)

    def runtimeError(error):
        print("{}\n[line {}]".format(error.message, error.token.line))
        Error.hadRuntimeError = True

    def tokenError(token, message):
        if token.type == TokenType.EOF:
            Error.report(token.line, " at end ", message)
        else:
            Error.report(token.line, " at '{}'".format(token.lexeme), message)

    def report(line, where, message):
        print("[{}] Error {}: {}".format(line, where, message))
        Error.hadError = True
