import importlib
from abc import ABC, abstractmethod


class Checker(ABC):
    @abstractmethod
    def check(self, value):
        raise NotImplementedError

    @abstractmethod
    def help(self) -> str:
        raise NotImplementedError


def get_checker(checker):
    if checker in DEFAULT_CHECKERS:
        return DEFAULT_CHECKERS[checker]

    if not isinstance(checker, Checker):
        raise TypeError("Invalid checker")

    return checker

class Int(Checker):
    def check(self, value):
        return int(value)

    def help(self):
        return "an int"

class Bool(Checker):
    def check(self, value):
        return bool(value)

    def help(self):
        return "a boolean"


class Float(Checker):
    def check(self, value):
        return float(value)

    def help(self):
        return "a float"


class Str(Checker):
    def check(self, value):
        if isinstance(value, str):
            return value
        raise TypeError()

    def help(self):
        return "a string"


class Anything(Checker):
    def check(self, value):
        return value

    def help(self):
        return "anything"


class Or(Checker):

    def __init__(self, *checkers):
        self.checkers = [get_checker(x) for x in checkers]

    def check(self, value):
        for checker in self.checkers:
            try:
                return checker.check(value)
            except Exception as e:
                pass
        raise ValueError("None of the condition are valid")

    def help(self):
        return ' or '.join([x.help() for x in self.checkers])

class And(Checker):
    def __init__(self, *checkers):
        self.checkers = [get_checker(x) for x in checkers]

    def check(self, value):
        result = value
        for checker in self.checkers:
            result = checker.check(result)
        return result

    def help(self):
        return ' and '.join([x.help() for x in self.checkers])

class InRange(Checker):

    def __init__(self, min=float('-inf'), max=float('+inf')):
        self.low = min
        self.high = max

    def check(self, value):
        if value < self.low or value > self.high:
            raise ValueError()
        return value

    def help(self):
        return f"between {self.low} and {self.high}"

class OneOf(Checker):

    def __init__(self, possible_values):
        self.possible_values = set(possible_values)

    def check(self, value):
        if value not in self.possible_values:
            raise ValueError()
        return value

    def help(self):
        return f"One of [{', '.join([str(x) for x in self.possible_values])}]"

class Module(Checker):

    def __init__(self):
        pass

    def check(self, value):
        return importlib.import_module(value)

    def help(self):
        return "path to python module"

class ImportedObject(Checker):

    def __init__(self):
        pass

    def check(self, value):
        path = value.split('.')
        module = '.'.join(path[:-1])
        imported = importlib.import_module(module)
        return getattr(imported, path[-1])


    def help(self):
        return "path to python module and an object within"


DEFAULT_CHECKERS = {
    int: Int(),
    float: Float(),
    str: Str(),
    bool: Bool()
}

