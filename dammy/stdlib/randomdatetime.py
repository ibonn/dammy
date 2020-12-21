import time
import datetime
import random

from dammy.core import BaseGenerator

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
            self._end = datetime.datetime(year=datetime.MAXYEAR, month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        else:
            self._end = end

        self._format = date_format

    def generate_raw(self, dataset=None, localization=None):
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

    def generate(self, dataset=None, localization=None):

        """
        Generates a random datetime and formats it if a format string has been given

        Implementation of the generate() method from BaseGenerator.

        :param dataset: The dataset from which all referenced fields will be retrieved. It will be ignored
        :type dataset: :class:`dammy.db.DatasetGenerator` or dict
        :returns: A randomly generated datetime or a string representation of it
        """
        d = self.generate_raw(dataset)
        if self._format is None:
            return self._generate(d)
        else:
            return self._generate(d.strftime(self._format))