from token_2 import Token
from token_type import TokenType
from expression import Binary, Unary, Literal, Grouping


class AstPrinter:
    def print(self, expr):
        return expr.accept(self)

    def visitBinaryExpr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr):
        return self.parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visitUnaryExpr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *exprs):
        string_rep = f"({name}"
        for expr in exprs:
            string_rep += f" {expr.accept(self)}"
        string_rep += ")"
        return string_rep


if __name__ == "__main__":
    expression = Binary(
        Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67)),
    )
    print(AstPrinter().print(expression))
    expression = Binary(
        Literal(1),
        Token(TokenType.PLUS, "+", None, 1),
        Literal(2),
    )
    print(AstPrinter().print(expression))
