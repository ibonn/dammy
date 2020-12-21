"""
dammy generates fake data, either to populate your databases with dummy data or for any other purspose.
Datasets of any size can be easily generated and exported to SQL or as a dictionary.
"""

__all__ = ('stdlib', 'db', 'exceptions', 'functions')

from .core import seed
from .core import BaseGenerator, EntityGenerator, FunctionResult, AttributeGetter, MethodCaller, OperationResult
from .iterator import Iterator