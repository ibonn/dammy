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

        from dammy import DammyEntity
        from dammy.stdlib import RandomInteger

        class B(DammyEntity):
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

        from dammy import DammyEntity
        from dammy.db import ForeignKey
        from dammy.stdlib import RandomInteger

        class A(DammyEntity):
            attribute1 = RandomInteger(1, 10)
            attribute2 = RandomInteger(2, 5)

        class B(DammyEntity):
            attribute1 = RandomInteger(15, 546)
            reference_to_A = ForeignKey(A, 'attribute1')
    
    This exampe will raise a IntegrityException because reference_to_A in class B is a foreign key
    referencing the field attribute1 from class A, and A.attribute1 is not a primary key

    """
    pass