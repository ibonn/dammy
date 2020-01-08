class DammyException(Exception):
    pass

class BaseDammy:

    _last_generated = None

    def generate(self):
        raise DammyException('The generate() method must be overridden')

    def __add__(self, other):
        return MultiValuedDammy(self, other)

    def __str__(self):
        return self.generate()

class MultiValuedDammy(BaseDammy):
    def __init__(self, *args):
        self._values = args

class DammyEntity(BaseDammy):
    def __init__(self):
        self.attrs = [i for i, v in self.__class__.__dict__.items() if i[:1] != '_' and not callable(v)]

    def generate(self):
        return dict((attr, getattr(self, attr).generate()) for attr in self.attrs)

    def __iter__(self):
        for x in self.generate().items():
            yield x

    def __str__(self):
        return str(dict(self))