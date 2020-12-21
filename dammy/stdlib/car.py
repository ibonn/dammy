import json
import random
import pkg_resources

from dammy.db import ForeignKey
from dammy.core import BaseGenerator

class CarBrand(BaseGenerator):
    """
    Generates a random car brand
    """
    _brands = None

    def __init__(self):
        super(CarBrand, self).__init__('VARCHAR(15)')
        if CarBrand._brands is None:
            with pkg_resources.resource_stream('dammy', 'data/car_models.json') as f:
                CarBrand._brands = list(json.load(f).keys())

    def generate_raw(self, dataset=None, localization=None):
        """
        Generates a new car brand

        Implementation of the generate_raw() method from BaseGenerator.

        :param dataset: The dataset from which all referenced fields will be retrieved. It will be ignored
        :type dataset: :class:`dammy.db.DatasetGenerator` or dict
        :returns: A randomly chosen car manufacturer name
        """
        return self._generate(random.choice(CarBrand._brands))

class CarModel(BaseGenerator):
    """
    Generates a random car model given a car brand. If car_brand is missing, it will be chosen at random

    :param car_brand: The brand of the car
    :type car_brand: :class:`dammy.stdlib.CarBrand` or :class:`dammy.db.ForeignKey`
    """

    _models = None

    def __init__(self, car_brand=None):
        super(CarModel, self).__init__('VARCHAR(25)')
        self._car_brand = car_brand

        if CarModel._models is None:
            with pkg_resources.resource_stream('dammy', 'data/car_models.json') as f:
                CarModel._models = json.load(f)

    def generate_raw(self, dataset=None, localization=None):
        """
        Generates a new car model

        Implementation of the generate_raw() method from BaseGenerator.

        :param dataset: The dataset from which all referenced fields will be retrieved. It will be ignored
        :type dataset: :class:`dammy.db.DatasetGenerator` or dict
        :returns: A randomly chosen car model
        :raises: Exception
        """
        car_brand = self._car_brand
        if car_brand is None:
            car_brand = CarBrand().generate()
            while len(CarModel._models[car_brand]) == 0:
                car_brand = CarBrand().generate()

        elif isinstance(car_brand, CarBrand):
            car_brand = car_brand._last_generated

        elif isinstance(car_brand, ForeignKey):
            car_brand = list(car_brand._last_generated.values())[0]

        return self._generate(random.choice(CarModel._models[car_brand]))