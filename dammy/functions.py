"""
This module includes some standard functions to be used on dammy objects
"""

from .core import FunctionResult

def average(lst):
    """
    Get the average value of a list
    """
    def avg(lst):
        return sum(lst) / len(lst)
    return FunctionResult(avg, lst)

def maximum(lst):
    """
    Get the maximum value of a list
    """
    return FunctionResult(max, lst)

def minimum(lst):
    """
    Get the minimum value of a list
    """
    return FunctionResult(min, lst)

def cast(obj, t):
    """
    Casts an object to the specified type
    obj -> The object to be casted
    t -> The type
    """
    return FunctionResult(t, obj)