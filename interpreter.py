from token_type import TokenType
from error import Error
from custom_runtime_error import CustomRuntimeError
from environment import Environment
from lox_callable import LoxCallable, Clock
from lox_function import LoxFunction
from return_klass import Return
from lox_class import LoxClass
from lox_instance import LoxInstance


class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
        self.globals.define("clock", Clock())
        self.locals = {}

    def interpret(self, statements):
        try:
            for stmt in statements:
                self.execute(stmt)
        except CustomRuntimeError as err:
            Error.runtimeError(err)

    def execute(self, stmt):
        stmt.accept(self)

    def resolve(self, expr, depth):
        self.locals[expr] = depth

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

    def visitVariableExpr(self, expr):
        return self.lookUpVariable(expr.name, expr)

    def lookUpVariable(self, name, expr):
        distance = self.locals.get(expr)
        if distance is not None:
            return self.environment.getAt(distance, name.lexeme)
        return self.globals.get(name)

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

    def visitLogicalExpr(self, expr):
        left = self.evaluate(expr.left)
        if expr.operator == TokenType.OR:
            if isTruthy(left):
                return left
        if expr.operator == TokenType.AND:
            if not isTruthy(left):
                return left

        return self.evaluate(expr.right)

    def visitSetExpr(self, expr):
        obj = self.evaluate(expr.object)
        if not isinstance(obj, LoxInstance):
            raise CustomRuntimeError(expr.name, "Only instances have fields.")

        value = self.evaluate(expr.value)
        obj.set(expr.name, value)
        return value

    def visitSuperExpr(self, expr):
        distance = self.locals.get(expr)
        superclass = self.environment.getAt(distance, "super")
        obj = self.environment.getAt(distance - 1, "this")

        method = superclass.findMethod(expr.method.lexeme)
        if method is None:
            raise CustomRuntimeError(
                expr.method, f"Undefined property '{expr.method.name}'."
            )
        return method.bind(obj)

    def visitThisExpr(self, expr):
        return self.lookUpVariable(expr.keyword, expr)

    def visitCallExpr(self, expr):
        callee = self.evaluate(expr.callee)
        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        if not isinstance(callee, LoxCallable):
            raise CustomRuntimeError(expr.paren, "Can only call functions and classes.")

        if len(arguments) != callee.arity():
            raise CustomRuntimeError(
                expr.paren,
                f"Expected {callee.arity()} arguments but got {len(arguments)}.",
            )
        return callee.call(self, arguments)

    def visitGetExpr(self, expr):
        obj = self.evaluate(expr.object)
        if isinstance(obj, LoxInstance):
            return obj.get(expr.name)

        raise CustomRuntimeError(expr.name, "Only instances have properties.")

    def visitExpressionStmt(self, stmt):
        self.evaluate(stmt.expression)

    def visitFunctionStmt(self, stmt):
        function = LoxFunction(stmt, self.environment, False)
        self.environment.define(stmt.name.lexeme, function)

    def visitPrintStmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(str(value))

    def visitReturnStmt(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise Return(value)

    def visitWhileStmt(self, stmt):
        while isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visitVarStmt(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)

    def visitAssignExpr(self, expr):
        value = self.evaluate(expr.value)
        distance = self.locals.get(expr)
        if distance is not None:
            self.environment.assignAt(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)

    def visitBlockStmt(self, stmt):
        self.executeBlock(stmt.statements, Environment(enclosing=self.environment))

    def visitClassStmt(self, stmt):
        superclass = None
        if stmt.superclass is not None:
            superclass = self.evaluate(stmt.superclass)
            if not isinstance(superclass, LoxClass):
                raise CustomRuntimeError(
                    stmt.superclass.name, "Superclass must be a class."
                )

        self.environment.define(stmt.name.lexeme, None)

        if stmt.superclass is not None:
            self.environment = Environment(self.environment)
            self.environment.define("super", superclass)

        methods = {}
        for method in stmt.methods:
            function = LoxFunction(
                method,
                self.environment,
                method.name.lexeme == "init",
            )
            methods[method.name.lexeme] = function
        klass = LoxClass(stmt.name.lexeme, superclass, methods)

        if superclass is not None:
            self.environment = self.environment.enclosing

        self.environment.assign(stmt.name, klass)

    def visitIfStmt(self, stmt):
        if isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.execute(stmt.elseBranch)

    def executeBlock(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for stmt in statements:
                self.execute(stmt)
        finally:
            self.environment = previous


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
