from return_klass import Return
from environment import Environment
from lox_callable import LoxCallable


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
