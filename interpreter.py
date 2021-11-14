from tokenType import TokenType
from error import Error
from custom_runtime_error import CustomRuntimeError


class Interpreter:
    def interpret(self, expression):
        try:
            value = self.evaluate(expression)
            print(stringify(value))
        except CustomRuntimeError as err:
            Error.runtimeError(err)

    def evaluate(self, expr):
        return expr.accept(self)

    def visitLiteralExpr(self, expr):
        return expr.value

    def visitGroupingExpr(self, expr):
        return self.evaluate(expr.expression)

    def visitUnaryExpr(self, expr):
        right = self.evaluate(expr.right)

        operator_type = expr.operator.type
        if operator_type == TokenType.MINUS:
            checkNumberOperand(expr.operator, right)
            return -1 * right
        if operator_type == TokenType.BANG:
            return not isTruthy(right)

        # Unreachable
        return None

    def visitBinaryExpr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        operator_type = expr.operator.type
        if operator_type == TokenType.MINUS:
            checkNumberOperands(expr.operator, left, right)
            return left - right
        if operator_type == TokenType.SLASH:
            checkNumberOperands(expr.operator, left, right)
            return left / right
        if operator_type == TokenType.STAR:
            checkNumberOperands(expr.operator, left, right)
            return left * right
        if operator_type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            raise CustomRuntimeError(
                expr.operator, "Operands must be two numbers or two strings."
            )
        if operator_type == TokenType.GREATER:
            checkNumberOperands(expr.operator, left, right)
            return left > right
        if operator_type == TokenType.GREATER_EQUAL:
            checkNumberOperands(expr.operator, left, right)
            return left >= right
        if operator_type == TokenType.LESS:
            checkNumberOperands(expr.operator, left, right)
            return left < right
        if operator_type == TokenType.LESS_EQUAL:
            checkNumberOperands(expr.operator, left, right)
            return left <= right
        if operator_type == TokenType.BANG_EQUAL:
            return not isEqual(left, right)
        if operator_type == TokenType.EQUAL_EQUAL:
            return isEqual(left, right)
        # Unreachable
        return None


def stringify(value):
    if value is None:
        return "nil"
    return str(value)


def isTruthy(value):
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    return True


def isEqual(left, right):
    if left is None and right is None:
        return True
    if left is None:
        return False
    return left == right


def checkNumberOperand(operator, operand):
    if isinstance(operand, float):
        return
    raise CustomRuntimeError(operator, "Operand must be a number")


def checkNumberOperands(operator, left, right):
    if isinstance(left, float) and isinstance(right, float):
        return
    raise CustomRuntimeError(operator, "Operands must be numbers.")
