"""
This module contains all classes needed to create new classes compatible with dammy,
the dataset generator used to generate datasets (DatasetGenerator) and the exception
fromm all dammy exceptions inherit (DammyException)
"""

from .DatasetGenerator import DatasetGenerator
from .core import BaseDammy, DammyEntity, FunctionResult, AttributeGetter, MethodCaller, DammyGenerator