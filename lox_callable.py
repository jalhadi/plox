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


# Native functions
class Clock:
    def call(self, interpreter, arguments):
        return time.time()

    def arity(self):
        return 0

    def toString(self):
        return "<native fn>"
