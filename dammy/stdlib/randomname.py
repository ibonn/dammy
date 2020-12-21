import json
import random
import pkg_resources

from dammy.core import BaseGenerator

class RandomName(BaseGenerator):
    """
    Generates a random name given a gender (optional)
    If gender not given, it will be chosen at random

    :param gender: The gender of the name. Either 'male' or 'female'.
    :type gender: str
    """

    _names = None

    def __init__(self, gender=None):
        super(RandomName, self).__init__('VARCHAR(15)')
        self._gender = gender

        if RandomName._names is None:
            with pkg_resources.resource_stream('dammy', 'data/names.json') as f:
                RandomName._names = json.load(f)

    def generate_raw(self, dataset=None, localization=None):
        """
        Generates a new random name

        Implementation of the generate_raw() method from BaseGenerator.

        :param dataset: The dataset from which all referenced fields will be retrieved. It will be ignored
        :type dataset: :class:`dammy.db.DatasetGenerator` or dict
        :returns: A person name, chosen at random
        """
        gender = self._gender
        if gender is None:
            gender = random.choice(['male', 'female'])

        if localization is None or localization.lower() == 'default':
            localization = random.choice(list(RandomName._names.keys()))
        elif localization not in RandomName._names.keys():
            localization = 'default'
        
        return self._generate(random.choice(RandomName._names[localization][gender]))