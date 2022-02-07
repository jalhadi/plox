from lox_callable import LoxCallable
from lox_instance import LoxInstance


class LoxClass(LoxCallable):
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods

    def call(self, interpreter, arguments):
        instance = LoxInstance(self)
        initializer = self.findMethod("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)
        return instance

    def findMethod(self, name):
        return self.methods.get(name)

    def arity(self):
        initializer = self.findMethod("init")
        if initializer is None:
            return 0
        return initializer.arity()

    def __str__(self):
        return self.name
