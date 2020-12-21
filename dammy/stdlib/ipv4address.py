import random

from dammy.core import BaseGenerator

class IPV4Address(BaseGenerator):
    """
    Generates a random IPv4 address
    """

    def __init__(self):
        super(IPV4Address, self).__init__('VARCHAR(15)')

    def generate_raw(self, dataset=None, localization=None):
        """
        Generates a random IPv4 address

        Implementation of the generate_raw() method from BaseGenerator.

        :param dataset: The dataset from which all referenced fields will be retrieved. It will be ignored
        :type dataset: :class:`dammy.db.DatasetGenerator` or dict
        :returns: A randomly generated blood type
        """

        ip_address = IPV4Address.__generate_ip()

        # TODO check invalid ip addresses
        invalid_addr = [
            '0.0.0.0',
        ]

        while ip_address in invalid_addr:
            ip_address = IPV4Address.__generate_ip()

        return ip_address

    @staticmethod
    def __generate_ip():
        return '.'.join([str(random.randint(0, 254)) for i in range(4)])