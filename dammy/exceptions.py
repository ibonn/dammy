"""
This module contains all the custom exceptions used by dammy.
"""
class DammyException(Exception):
    """
    The base exception from which all dammy exceptions inherit

    .. note::
        This exception should not be raised by any means. Its only purpose is to check
        in a try-catch block wether an exception has been raised by dammy or not.
    """
    pass

class DatasetRequiredException(DammyException):
    """
    This exception is raised when a generator requires a dataset to get references from it but
    no dataset is given

    Example::

        from dammy import EntityGenerator
        from dammy.stdlib import RandomInteger

        class B(EntityGenerator):
            attribute1 = RandomInteger(15, 546)
            reference_to_A = ForeignKey(A, 'attribute1')

        B().generate()  # generate() requires a dataset because B contains a reference to another generator
                        # thus, this call will result in a DatasetRequiredException
    """
    pass

class IntegrityException(DammyException):
    """
    Raised when database integrity rules are violated

    Example::

        from dammy import EntityGenerator
        from dammy.db import ForeignKey
        from dammy.stdlib import RandomInteger

        class A(EntityGenerator):
            attribute1 = RandomInteger(1, 10)
            attribute2 = RandomInteger(2, 5)

        class B(EntityGenerator):
            attribute1 = RandomInteger(15, 546)
            reference_to_A = ForeignKey(A, 'attribute1')

    This example will raise a IntegrityException because reference_to_A in class B is a foreign key
    referencing the field attribute1 from class A, and A.attribute1 is not a primary key
    """
    pass

class MaximumRetriesExceededException(DammyException):
    """
    Raised when a unique field exceeds the maximum number of retries to generate a unique value

    This is commonly raised when the amount of generated data is bigger than the available data
    on a generator obtaining its data from a file.

    Example::

        from dammy.db import Unique
        from dammy.stdlib import RandomInteger

        x = Unique(RandomInteger(1, 10))

        for i in range(0, 50):
            print(x)            # Exception after generating 10 values

    The code will result in an exception because it will try to generate 50 unique integers in the [1, 10]
    interval, which is obviously impossible because there are 10 unique integers available
    """
    pass

class InvalidReferenceException(DammyException):
    """
    Raised when a foreign key references a field which is not a primary key or unique

    This is commonly raised when the amount of generated data is bigger than the available data
    on a generator obtaining its data from a file.
    """
    pass

class EmptyKeyException(DammyException):
    """
    Raised when a primary key or a unique filed is empty
    """
    pass