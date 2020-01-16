"""
This module contains all the dammy related exceptions
"""
class DammyException(Exception):
    """
    The base exception from which all dammy exceptions inherit
    """
    pass

class DatasetRequiredException(DammyException):
    """
    This exception is raised when a generator requires a dataset to get references from it but
    no dataset is given
    """
    pass

class IntegrityException(DammyException):
    """
    Raised when database integrity rules are violated
    """
    pass