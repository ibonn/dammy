import json
import random

from core import BaseDammy

class RandomInteger(BaseDammy):
    """
    Generates a random integer in the given interval
    """

    def __init__(self, lb, ub):
        self._lb = lb
        self._ub = ub

    def generate(self):
        return random.randint(self._lb, self._ub)

class RandomName(BaseDammy):
    """
    Generates a random name given a language code and a gender (optional)
    If gender not given, it will be chosen at random
    """

    _names = None

    def __init__(self, language_code, gender=None):
        self._language_code = language_code
        self._gender = gender

        if RandomName._names is None:
            with open('data/names.json') as f:
                RandomName._names = json.load(f)

    def generate(self):
        gender = self._gender
        if gender is None:
            gender = random.choice(['male', 'female'])
        return random.choice(RandomName._names[self._language_code][gender])

# TODO
class CityName(BaseDammy):
    """
    Generates a random city name given a country code (using the ISO 3166-1 standard) (optional)
    and a state/province code (using the ISO 3166-2 standard) (optional)
    If any of the parameters are not given, it will be chosen at random
    """

    def __init__(self, country_code=None, subdivision_code=None):
        self._country_code = country_code

    def generate(self):
        return ''

class RandomString(BaseDammy):
    """
    Generates a random string with the given length and symbols. 
    The default symbols are all the letters in the english alphabet (both uppercase and lowercase) and numbers 0 through 9
    """

    def __init__(self, length, symbols="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
        self._length = length
        self._symbols = list(symbols)

    def generate(self):
        return ''.join(random.choice(self._symbols) for i in range(self._length))

# TODO
class RandomDate(BaseDammy):
    """
    Generates a random date in the given interval using the given format.
    The default start date is datetime.MINYEAR
    The default end date is datetime.MAXYEAR
    If format is not supplied, a datetime object will be generated
    """
    def __init__(self, start=None, end=None, format=None):
        self._start = start
        self._end = end

    def generate(self):
        return ''

class CarBrand(BaseDammy):
    """
    Generates a random car brand
    """
    _brands = None

    def __init__(self):
        if CarBrand._brands is None:
            with open('data/car_models.json') as f:
                CarBrand._brands = list(json.load(f).keys())

    def generate(self):
        CarBrand._last_generated = random.choice(CarBrand._brands)
        return CarBrand._last_generated

class CarModel(BaseDammy):
    """
    Generates a random car model given a car brand. If car_brand is missing, it will be chosen at random
    """

    _models = None

    def __init__(self, car_brand=None):
        self._car_brand = car_brand

        if CarModel._models is None:
            with open('data/car_models.json') as f:
                CarModel._models = json.load(f)

    def generate(self):
        car_brand = self._car_brand
        if car_brand is None:
            car_brand = CarBrand().generate()
            while len(CarModel._models[car_brand]) == 0:
                car_brand = CarBrand().generate()
        elif isinstance(car_brand, CarBrand):
            car_brand = CarBrand._last_generated
        
        return random.choice(CarModel._models[car_brand])