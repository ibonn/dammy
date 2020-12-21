import random

from dammy.core import BaseGenerator

class BloodType(BaseGenerator):
    """
    Generates a random blood type
    """

    def __init__(self):
        super(BloodType, self).__init__('VARCHAR(3)')

    def generate_raw(self, dataset=None, localization=None):
        """
        Generates a random blood type

        Implementation of the generate_raw() method from BaseGenerator.

        :param dataset: The dataset from which all referenced fields will be retrieved. It will be ignored
        :type dataset: :class:`dammy.db.DatasetGenerator` or dict
        :returns: A randomly generated blood type
        """

        letters = ['A', 'B', '0', 'AB']
        symbols = ['+', '-']

        return self._generate(random.choice(letters) + random.choice(symbols))