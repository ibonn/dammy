import json
import random
import time
import datetime

from db import ForeignKey
from core import BaseDammy, get_reference

class RandomInteger(BaseDammy):
    """
    Generates a random integer in the given interval
    """

    def __init__(self, lb, ub):
        super(RandomInteger, self).__init__('INTEGER')
        self._lb = lb
        self._ub = ub

    """
    Generates a new random integer
    """
    def generate(self, dataset=None):
        return self._generate(random.randint(self._lb, self._ub))

class RandomName(BaseDammy):
    """
    Generates a random name given a language code and a gender (optional)
    If gender not given, it will be chosen at random
    """

    _names = None

    def __init__(self, language_code, gender=None):
        super(RandomName, self).__init__('VARCHAR(15)')
        self._language_code = language_code
        self._gender = gender

        if RandomName._names is None:
            with open('data/names.json') as f:
                RandomName._names = json.load(f)

    """
    Generates a new random name
    """
    def generate(self, dataset=None):
        gender = self._gender
        if gender is None:
            gender = random.choice(['male', 'female'])
        return self._generate(random.choice(RandomName._names[self._language_code][gender]))

# TODO
class CountryName(BaseDammy):
    """
    Generates a random country name
    """

    _countries = None

    def __init__(self):
        super(CountryName, self).__init__('VARCHAR(50)')

        if CountryName._countries is None:
            with open('data/countries.json') as f:
                CountryName._countries = json.load(f)

    """
    Generates a new country name
    """
    def generate(self, dataset=None):
        c = random.choice(list(CountryName._countries.keys()))
        return self._generate(CountryName._countries[c])

class RandomString(BaseDammy):
    """
    Generates a random string with the given length and symbols. 
    The default symbols are all the letters in the english alphabet (both uppercase and lowercase) and numbers 0 through 9
    """

    def __init__(self, length, symbols="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
        super(RandomString, self).__init__('VARCHAR({})'.format(length))
        self._length = length
        self._symbols = list(symbols)

    """
    Generates a new random string
    """
    def generate(self, dataset=None):
        return self._generate(''.join(random.choice(self._symbols) for i in range(self._length)))

class TimeDeltaGenerator(BaseDammy):
    """
    This class is not intended for regular usage. 
    It is used to allow random datetime addition/substraction and returned when such operation is performed
    """
    def __init__(self, a, b, op):
        super(TimeDeltaGenerator, self).__init__('DATETIME')
        self.operator = op
        self.dt1 = a
        self.dt2 = b

    def generate(self, dataset=None):
        if isinstance(self.dt1, RandomDateTime):
            dt1 = self.dt1.generate()
        else:
            dt1 = self.dt1

        if isinstance(self.dt2, RandomDateTime):
            dt2 = self.dt2.generate()
        else:
            dt2 = self.dt2

        if self.operator == '+':
            return self._generate(dt1 + dt2)
        elif self.operator == '-':
            return self._generate(dt1 - dt2)
        else:
            # TODO
            raise Exception()

class RandomDateTime(BaseDammy):
    """
    Generates a random datetime in the given interval using the given format.
    The default start date is datetime.MINYEAR (january 1st)
    The default end date is datetime.MAXYEAR (december 31st)
    If format is not supplied, a datetime object will be generated
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

    def __sub__(self, other):
        """
        datetime substraction
        """
        if isinstance(other, RandomDateTime):
            # A new RandomDateTime object is created without format to avoid genearting a string on the generator
            return TimeDeltaGenerator(RandomDateTime(self._start, self._end), other, '-')

        return NotImplemented

    def __rsub__(self, other):
        """
        datetime substraction alternative
        """
        if isinstance(other, datetime.datetime):
            return TimeDeltaGenerator(other, RandomDateTime(self._start, self._end), '-')
        return NotImplemented

    def __add__(self, other):
        """
        datetime addition
        """
        if isinstance(other, RandomDateTime):
            return TimeDeltaGenerator(RandomDateTime(self._start, self._end), other, '+')
            
        return NotImplemented
    
    def __radd__(self, other):
        """
        datetime addition alternative
        """
        if isinstance(other, datetime.datetime):
            return TimeDeltaGenerator(other, RandomDateTime(self._start, self._end), '+')
        return NotImplemented

    def generate(self, dataset=None):
        """
        Generates a new random datetime
        """
        s = time.mktime(self._start.timetuple())
        e = time.mktime(self._end.timetuple())
        t = random.uniform(s, e)
        if self._format is None:
            return self._generate(datetime.datetime.fromtimestamp(t))
        else:
            return self._generate(time.strftime(self._format, time.localtime(t)))

class CarBrand(BaseDammy):
    """
    Generates a random car brand
    """
    _brands = None

    def __init__(self):
        super(CarBrand, self).__init__('VARCHAR(15)')
        if CarBrand._brands is None:
            with open('data/car_models.json') as f:
                CarBrand._brands = list(json.load(f).keys())

    """
    Generates a new car brand
    """
    def generate(self, dataset=None):
        return self._generate(random.choice(CarBrand._brands))

class CarModel(BaseDammy):
    """
    Generates a random car model given a car brand. If car_brand is missing, it will be chosen at random
    """

    _models = None

    def __init__(self, car_brand=None):
        super(CarModel, self).__init__('VARCHAR(25)')
        self._car_brand = car_brand

        if CarModel._models is None:
            with open('data/car_models.json') as f:
                CarModel._models = json.load(f)

    """
    Generates a new car model
    """
    def generate(self, dataset=None):
        car_brand = self._car_brand
        if car_brand is None:
            car_brand = CarBrand().generate()
            while len(CarModel._models[car_brand]) == 0:
                car_brand = CarBrand().generate()

        elif isinstance(car_brand, CarBrand):
            car_brand = car_brand._last_generated

        elif isinstance(car_brand, ForeignKey):
            car_brand = get_reference(car_brand, dataset)

        return self._generate(random.choice(CarModel._models[car_brand]))