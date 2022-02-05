from custom_runtime_error import CustomRuntimeError


class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        self.values[name] = value

    def assign(self, name, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise CustomRuntimeError(name, f"Undefined variable '{name.lexeme}.'")

    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise CustomRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def getAt(self, distance, name):
        return self.ancestor(distance).values.get(name)

    def assignAt(self, distance, name, value):
        self.ancestor(distance).values[name.lexeme] = value

    def ancestor(self, distance):
        environment = self
        for i in range(distance):
            environment = environment.enclosing
        return environment
