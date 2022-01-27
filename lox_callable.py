import time

from return_klass import Return
from environment import Environment


class LoxCallable:
    def call(self, interpreter, arguments):
        raise NotImplementedError

    def arity(self):
        raise NotImplementedError

    def toString(self):
        raise NotImplementedError


class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter, arguments):
        environment = Environment(enclosing=self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(
                self.declaration.params[i].lexeme,
                arguments[i],
            )
        try:
            interpreter.executeBlock(self.declaration.body, environment)
        except Return as returnValue:
            return returnValue.value

    def arity(self):
        return len(self.declaration.params)

    def toString(self):
        return f"<fn {self.declaration.name.lexeme}>"


# Native functions
class Clock:
    def call(self, interpreter, arguments):
        return time.time()

    def arity(self):
        return 0

    def toString(self):
        return "<native fn>"
