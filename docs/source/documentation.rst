.. _documentation:

Documentation
**************************
You can access the basic classes by just importing dammy::

    import dammy

But if you want to add more functionality, there are more modules available.
 Check the documentation page for each module to see the available classes and
functions.

.. currentmodule:: dammy

.. autosummary::

   db
   exceptions
   functions
   stdlib

The main module
===================
The classes in the main module are listed below.

.. currentmodule:: dammy

.. autoclass:: BaseGenerator
    :members:

.. autoclass:: EntityGenerator
    :members:
    :inherited-members:

.. autoclass:: FunctionResult
    :members:
    :inherited-members:

.. autoclass:: AttributeGetter
    :members:
    :inherited-members:

.. autoclass:: MethodCaller
    :members:
    :inherited-members:

.. autoclass:: OperationResult
    :members:
    :inherited-members:

More modules
===================
In addition to the main module, dammy contains other modules extending the functionalities

.. toctree::
    :maxdepth: 2

    db
    functions
    stdlib
    exceptions