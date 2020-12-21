import random

from dammy.core import BaseGenerator

class RandomInteger(BaseGenerator):
    """
    Generates a random integer in the given interval

    :param lb: The lower bound of the inteval
    :param ub: The upper bound of the interval
    :type lb: int
    :type ub: int

    Example::
        RandomInteger(0, 5) # Will return a random integer generator in the [0, 5] interval
    """

    def __init__(self, lb, ub):
        super(RandomInteger, self).__init__('INTEGER')
        self._lb = lb
        self._ub = ub

    def generate_raw(self, dataset=None, localization=None):
        """
        Generates a new random integer

        Implementation of the generate_raw() method from BaseGenerator.

        :param dataset: The dataset from which all referenced fields will be retrieved. It will be ignored
        :type dataset: :class:`dammy.db.DatasetGenerator` or dict
        :returns: A random integer
        """
        return self._generate(random.randint(self._lb, self._ub))