import random

from dammy.core import BaseGenerator

class RandomString(BaseGenerator):
    """
    Generates a random string with the given length and symbols.
    The default symbols are all the letters in the english alphabet (both uppercase and lowercase) and numbers 0 through 9

    :param length: The length of the string
    :param symbols: The simbols available to generate the string
    :type length: int
    :type symbols: str, list or tuple
    """

    def __init__(self, length, symbols="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
        super(RandomString, self).__init__('VARCHAR({})'.format(length))
        self._length = length
        self._symbols = list(symbols)

    def generate_raw(self, dataset=None, localization=None):
        """
        Generates a new random string

        Implementation of the generate_raw() method from BaseGenerator.

        :param dataset: The dataset from which all referenced fields will be retrieved. It will be ignored
        :type dataset: :class:`dammy.db.DatasetGenerator` or dict
        :returns: A randomly generated string
        """
        return self._generate(''.join(random.choice(self._symbols) for i in range(self._length)))