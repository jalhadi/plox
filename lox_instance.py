from custom_runtime_error import CustomRuntimeError


class LoxInstance:
    def __init__(self, klass):
        self.klass = klass
        self.fields = {}

    def get(self, name):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        method = self.klass.findMethod(name.lexeme)
        if method is not None:
            return method.bind(self)

        raise CustomRuntimeError(name, f"Undefined property '{name.lexeme}'.")

    def set(self, name, value):
        self.fields[name.lexeme] = value

    def __str__(self):
        return f"{self.klass.name} instance"
