from core import BaseDammy

class AutoIncrement(BaseDammy):
    """
    Represents an automatically incrementing field. By default starts by 1 and increments by 1
    """

    def __init__(self, start=1, increment=1):
        super(AutoIncrement, self).__init__('INTEGER')
        if self._last_generated is None:
            self._last_generated = start - 1
        self._increment = increment

    """
    Generates and updates the next value
    """
    def generate(self, dataset=None):
        return self._generate(self._last_generated + 1)