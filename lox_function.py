from return_klass import Return
from environment import Environment
from lox_callable import LoxCallable


class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure, isInitializer):
        self.declaration = declaration
        self.closure = closure
        self.isInitializer = isInitializer

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
            if self.isInitializer:
                return self.closure.getAt(0, "this")
            return returnValue.value

        if self.isInitializer:
            return self.closure.getAt(0, "this")

    def bind(self, instance):
        environment = Environment(self.closure)
        environment.define("this", instance)
        return LoxFunction(
            self.declaration,
            environment,
            self.isInitializer,
        )

    def arity(self):
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"
