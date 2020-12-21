import random

from dammy.core import BaseGenerator

class CreditCard(BaseGenerator):
    """
    Generates a random credit card number
    """

    def __init__(self):
        super(CreditCard, self).__init__('VARCHAR(15)')

    def generate_raw(self, dataset=None, localization=None):
        """
        Generates a random credit card number

        Implementation of the generate_raw() method from BaseGenerator.

        :param dataset: The dataset from which all referenced fields will be retrieved. It will be ignored
        :type dataset: :class:`dammy.db.DatasetGenerator` or dict
        :returns: A randomly generated blood type
        """

        num = CreditCard.__generate_number()

        while not CreditCard.__validate(num):
            num = CreditCard.__generate_number()

        return num

    @staticmethod
    def __generate_number():
        """
        Generate a 16 digit credit card number candidate, formatted with spaces every 4 digits

        :returns: A synthetic credit card number
        """
        return ' '.join(['{:04d}'.format(random.randint(0, 9999)) for i in range(4)])

    @staticmethod
    def __validate(number):
        """
        Uses Luhn algorithm to check wether a number is a valid credit card number or not

        :param number: The number to validate
        :returns: True on success, false otherwise
        """
        digits = [int(d) for d in number.replace(' ', '')]
        even_pos = digits[1::2]
        odd_pos  = digits[::2]

        double_digits = [2 * d for d in even_pos]

        s = sum(odd_pos)
        for x in double_digits:
            m = x % 10
            d = (x - m) // 10
            s += m + d
        
        return s % 10 == 0