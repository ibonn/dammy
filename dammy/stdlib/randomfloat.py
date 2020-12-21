import random

from dammy.core import BaseGenerator

class RandomFloat(BaseGenerator):
    """
    Generates a random floating point number in the given interval

    :param lb: The lower bound of the inteval
    :param ub: The upper bound of the interval
    :type lb: float
    :type ub: float

    Example::
        RandomFloat(0.8, 2.87) # Will return a random integer generator in the [0.8, 2.87] interval
    """

    def __init__(self, lb, ub):
        super(RandomFloat, self).__init__('DECIMAL')
        self._lb = lb
        self._ub = ub

    def generate_raw(self, dataset=None, localization=None):
        """
        Generates a new random floating point number

        Implementation of the generate_raw() method from BaseGenerator.

        :param dataset: The dataset from which all referenced fields will be retrieved. It will be ignored
        :type dataset: :class:`dammy.db.DatasetGenerator` or dict
        :returns: A random integer
        """
        return self._generate(self._lb + random.random() * (self._ub - self._lb))