"""
This module includes some standard functions to be used on dammy objects
"""

from .core import FunctionResult

def average(lst):
    """
    Get the average value of a list

    :param lst: A list containing numeric values
    :type lst: list
    :returns: :class:`dammy.FunctionResult`
    """
    def avg(lst):
        return sum(lst) / len(lst)
    return FunctionResult(avg, lst)

def maximum(lst):
    """
    Get the maximum value of a list

    :param lst: A list containing numeric values
    :type lst: list
    :returns: :class:`dammy.FunctionResult`
    """
    return FunctionResult(max, lst)

def minimum(lst):
    """
    Get the minimum value of a list

    :param lst: A list containing numeric values
    :type lst: list
    :returns: :class:`dammy.FunctionResult`
    """
    return FunctionResult(min, lst)

def cast(obj, t):
    """
    Casts an object to the specified type

    :param obj: The object to cast
    :param t: The type
    :returns: :class:`dammy.FunctionResult`
    """
    return FunctionResult(t, obj)