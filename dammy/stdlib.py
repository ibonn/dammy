"""
This module contains some basic and common utilities, such as random generation for
person names, countries, integers, strings, dates...
"""
import json
import random
import time
import datetime
import pkg_resources

from .db import ForeignKey
from .core import BaseGenerator

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

    def generate_raw(self, dataset=None):
        """
        Generates a new random integer

        Implementation of the generate_raw() method from BaseGenerator. 

        :param dataset: The dataset from which all referenced fields will be retrieved. It will be ignored
        :type dataset: :class:`dammy.db.DatasetGenerator` or dict
        :returns: A random integer
        """
        return self._generate(random.randint(self._lb, self._ub))

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

    def generate_raw(self, dataset=None):
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
        return self._generate(random.choice(RandomName._names[gender]))

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


    def generate_raw(self, dataset=None):
        """
        Generates a new country name
        Implementation of the generate_raw() method from BaseGenerator. 

        :param dataset: The dataset from which all referenced fields will be retrieved. It will be ignored
        :type dataset: :class:`dammy.db.DatasetGenerator` or dict
        :returns: A country name, chosen at random
        """
        c = random.choice(list(CountryName._countries.keys()))
        return self._generate(CountryName._countries[c])

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

    def generate_raw(self, dataset=None):
        """
        Generates a new random string

        Implementation of the generate_raw() method from BaseGenerator. 

        :param dataset: The dataset from which all referenced fields will be retrieved. It will be ignored
        :type dataset: :class:`dammy.db.DatasetGenerator` or dict
        :returns: A randomly generated string
        """
        return self._generate(''.join(random.choice(self._symbols) for i in range(self._length)))

class RandomDateTime(BaseGenerator):
    """
    Generates a random datetime in the given interval using the given format.
    The default start date is datetime.MINYEAR (january 1st)
    The default end date is datetime.MAXYEAR (december 31st)
    If format is not supplied, a datetime object will be generated

    :param start: The lower bound of the interval
    :param end: The upper bound of the interval
    :param date_format: datetime.strftime() compatible format string
    :type start: datetime
    :type end: datetime
    :type date_format: str
    """

    def __init__(self, start=None, end=None, date_format=None):
        super(RandomDateTime, self).__init__('DATETIME')
        if start is None:
            self._start = datetime.datetime(year=datetime.MINYEAR, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            self._start = start

        if end is None:
            self._end = datetime.datetime(year=datetime.MAXYEAR, month=12, day=31, hour=23, minute=59, second=59, microsecond=9999999)
        else:
            self._end = end

        self._format = date_format

    def generate_raw(self, dataset=None):
        """
        Generates a new random datetime

        Implementation of the generate_raw() method from BaseGenerator. 

        :param dataset: The dataset from which all referenced fields will be retrieved. It will be ignored
        :type dataset: :class:`dammy.db.DatasetGenerator` or dict
        :returns: A randomly generated datetime
        """
        s = time.mktime(self._start.timetuple())
        e = time.mktime(self._end.timetuple())
        t = random.uniform(s, e)

        return self._generate(datetime.datetime.fromtimestamp(t))

    def generate(self, dataset=None):

        """
        Generates a random datetime and formats it if a format string has been given

        Implementation of the generate() method from BaseGenerator.

        :param dataset: The dataset from which all referenced fields will be retrieved. It will be ignored
        :type dataset: :class:`dammy.db.DatasetGenerator` or dict
        :returns: A randomly generated datetime or a string representation of it
        """
        d = self.generate_raw(dataset)
        if self._format is None:
            return d
        else:
            return d.strftime(self._format)

class BloodType(BaseGenerator):
    """
    Generates a random blood type
    """

    def __init__(self):
        super(BloodType, self).__init__('VARCHAR(3)')

    def generate_raw(self, dataset=None):
        """
        Generates a random blood type

        Implementation of the generate_raw() method from BaseGenerator. 

        :param dataset: The dataset from which all referenced fields will be retrieved. It will be ignored
        :type dataset: :class:`dammy.db.DatasetGenerator` or dict
        :returns: A randomly generated blood type
        """

        letters = ['A', 'B', '0', 'AB']
        symbols = ['+', '-']

        return random.choice(letters) + random.choice(symbols)

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

    def generate_raw(self, dataset=None):
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

    def generate_raw(self, dataset=None):
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