from enum import Enum, auto

from stmt import Stmt
from error import Error


class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()


class Resolver:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.currentFunction = FunctionType.NONE

    def visitBlockStmt(self, stmt):
        self.beginScope()
        self.resolve(stmt.statements)
        self.endScope()

    def resolve(self, obj):
        if isinstance(obj, list):
            statements = obj
            for statement in statements:
                self.resolve(statement)
        elif isinstance(obj, Stmt):
            # Single statment
            stmt = obj
            stmt.accept(self)
        else:
            # Single expression
            # Could be combined with above, but easier
            # to understand being split
            expr = obj
            expr.accept(self)

    def visitVarStmt(self, stmt):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)
        self.define(stmt.name)

    def visitFunctionStmt(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolveFunction(stmt, FunctionType.FUNCTION)

    def visitVariableExpr(self, expr):
        if len(self.scopes) != 0 and (self.scopes[-1].get(expr.name.lexeme) == False):
            Error.tokenError(
                expr.name, "Can't read local variable in its  own initializer"
            )

        self.resolveLocal(expr, expr.name)

    def visitAssignExpr(self, expr):
        self.resolve(expr.value)
        self.resolveLocal(expr, expr.name)

    def resolveLocal(self, expr, name):
        for i in reversed(range(len(self.scopes))):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return

    def visitExpressionStmt(self, stmt):
        self.resolve(stmt.expression)

    def visitIfStmt(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.thenBranch)
        if stmt.elseBranch is not None:
            self.resolve(stmt.elseBranch)

    def visitPrintStmt(self, stmt):
        self.resolve(stmt.expression)

    def visitReturnStmt(self, stmt):
        if self.currentFunction == TokenType.NONE:
            Error.tokenError(stmt.keyword, "Can't return from top-level code.")

        if stmt.value is not None:
            self.resolve(stmt.value)

    def visitWhileStmt(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)

    def visitCallExpr(self, expr):
        self.resolve(expr.callee)
        for argument in expr.arguments:
            self.resolve(argument)

    def visitGroupingExpr(self, expr):
        self.resolve(expr.expression)

    def visitLiteralExpr(self, expr):
        # Don't need to do anything when visiting
        # a literal expression
        pass

    def visitLogicalExpr(self, expr):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visitUnaryExpr(self, expr):
        self.resolve(expr.right)

    def resolveFunction(self, function, functionType):
        enclosingFunction = self.currentFunction
        self.currentFunction = functionType
        self.beginScope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.endScope()
        self.currentFunction = enclosingFunction

    def define(self, name):
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        scope[name.lexeme] = True

    def declare(self, name):
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        if name.lexeme in scope:
            Error.tokenError(name, "Already a variable with this name in this scope.")
        scope[name.lexeme] = False

    def beginScope(self):
        self.scopes.append({})

    def endScope(self):
        self.scopes.pop()
