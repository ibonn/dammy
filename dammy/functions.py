"""
This module includes some standard functions to be used on dammy objects
"""

from .core import FunctionResult

def call_function(obj, fun, *args, **kwargs):
    """
    Call a user given function. This function is useful when none of the available functions
    fulfills the task the user wants, so the user can feed the desired function here.

    :param obj: The object on which the function will be called
    :param fun: The function to call
    :param args: Comma separated arguments for the function
    :param kwargs: Comma separated keyword identified arguments for the function
    :type obj: BaseDammy
    :type fun: callable
    :returns: :class:`dammy.FunctionResult`
    """

    return FunctionResult(fun, obj, *args, **kwargs)

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