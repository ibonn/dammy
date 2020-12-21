import json
import random
import pkg_resources

from dammy.core import BaseGenerator

class CountryName(BaseGenerator):
    """
    Generates a random country name
    """

    _countries = None

    def __init__(self):
        super(CountryName, self).__init__('VARCHAR(50)')

        if CountryName._countries is None:
            with pkg_resources.resource_stream('dammy', 'data/countries.json') as f:
                CountryName._countries = json.load(f)


    def generate_raw(self, dataset=None, localization=None):
        """
        Generates a new country name
        Implementation of the generate_raw() method from BaseGenerator.

        :param dataset: The dataset from which all referenced fields will be retrieved. It will be ignored
        :type dataset: :class:`dammy.db.DatasetGenerator` or dict
        :returns: A country name, chosen at random
        """
        if localization is None or localization.lower() == 'default':
            localization = 'en'

        c = random.choice(list(CountryName._countries[localization].keys()))

        return self._generate(CountryName._countries[localization][c])