"""
This module contains the most important dammy classes. Ideally it should be separated
in 2 modules (core, db) but the dependencies between them make this impossible without
causing circular imports
"""
import random
from .DatasetGenerator import DatasetGenerator
from .exceptions import DatasetRequiredException, IntegrityException


############################         CORE            ############################
class BaseDammy:
    """
    The base class from which all generators must inherit.
    """
    def __init__(self, sql_equivalent):
        self._last_generated = None
        self._sql_equivalent = sql_equivalent

    def generate_raw(self, dataset=None):
        """
        Generate without posterior treatment. All generators must implement this method
        If a method does not implement this method a NotImplementedError will be raised
        """
        raise NotImplementedError('The generate_raw() method must be overridden')

    def generate(self, dataset=None):
        """
        Generate a value and perform a posterior treatment. By default, no treatment is done
        and generate_raw() is called.
        """
        return self.generate_raw(dataset)

    def _generate(self, value):
        """
        Updates the last generated value
        """
        self._last_generated = value
        return value

    def __add__(self, other):
        """
        Performs the addition of 2 BaseDammy objects
        """
        return DammyGenerator(self, other, '+', self._sql_equivalent)

    def __sub__(self, other):
        """
        Performs the substraction of 2 BaseDammy objects
        """
        return DammyGenerator(self, other, '-', self._sql_equivalent)

    def __mul__(self, other):
        """
        Performs the multiplication of 2 BaseDammy objects
        """
        return DammyGenerator(self, other, '*', self._sql_equivalent)

    def __mod__(self, other):
        """
        Performs the modulus of 2 BaseDammy objects
        """
        return NotImplemented

    def __floordiv__(self, other):
        """
        Performs the integer division of 2 BaseDammy objects
        """
        return NotImplemented

    def __truediv__(self, other):
        """
        Performs the true division of 2 BaseDammy objects
        """
        return DammyGenerator(self, other, '/', self._sql_equivalent)

    def __lt__(self, other):
        """
        Compares 2 BaseDammy objects to one another to check wether one is less than the other
        """
        return NotImplemented

    def __le__(self, other):
        """
        Compares 2 BaseDammy objects to one another to check wether one is less or equal than the other
        """
        return NotImplemented

    def __eq__(self, other):
        """
        Compares 2 BaseDammy objects to one another to check wether one is equal to the other
        """
        return NotImplemented

    def __ne__(self, other):
        """
        Compares 2 BaseDammy objects to one another to check wether one is not equal the other
        """
        return NotImplemented

    def __gt__(self, other):
        """
        Compares 2 BaseDammy objects to one another to check wether one is greater than the other
        """
        return NotImplemented

    def __ge__(self, other):
        """
        Compares 2 BaseDammy objects to one another to check wether one is greater or equal than the other
        """
        return NotImplemented

    def __str__(self):
        """
        Returns the string representation of the object. By default this value corresponds to the value of a
        randomly generated object without a dataset. It can raise a DatasetRequiredException if a dataset is required
        """
        return str(self.generate())

    def __getattr__(self, name):
        """
        Allows getting attribute values and calling methods on generators. See AttributeGetter
        """
        return AttributeGetter(self, name)


class DammyEntity(BaseDammy):
    """
    The class from which all composite generators must inherit. This class implements methods to keep
    generation easy
    """
    def __init__(self):
        items = self.__class__.__dict__.items()
        self.attrs = [i for i, v in items if i[:1] != '_' and not callable(v)]
        self.primary_key = [i for i, v in items if isinstance(v, PrimaryKey)]
        self.foreign_keys = [i for i, v in items if isinstance(v, ForeignKey)]


    def generate_raw(self, dataset=None):
        """
        Implementation of the generate_raw() method from BaseDammy. Gets all the attributes of the class
        and generates a new value
        """
        result = {}
        for attr in self.attrs:
            attr_obj = getattr(self, attr)

            # Get references to foreign keys
            if isinstance(attr_obj, ForeignKey):
                if dataset is None:
                    raise DatasetRequiredException(
                        'Reference to an entity ({}) given but no dataset containing {}s supplied'.format(
                            attr_obj.table_name,
                            attr_obj.table_name
                        )
                    )
                else:
                    if isinstance(dataset, DatasetGenerator):
                        while dataset._counters[attr_obj.table_name] != 0:
                            dataset._generate_entity(attr_obj.table_name)

                    chosen = random.choice(dataset[attr_obj.table_name])
                    if len(attr_obj) == 1:
                        result[attr] = chosen[attr_obj.ref_fields[0]]
                    else:
                        for n in attr_obj.ref_fields:
                            result['{}_{}'.format(attr, n)] = chosen[n]

            # Generate primary keys
            elif isinstance(attr_obj, PrimaryKey):
                result[attr] = attr_obj.field.generate(dataset)

            # Generate other fields
            elif isinstance(attr_obj, BaseDammy):
                result[attr] = attr_obj.generate(dataset)

            # Generate constant values
            else:
                result[attr] = attr_obj

        return result

############################ Generator manipulation  ############################
class FunctionResult(BaseDammy):
    """
    Allows the manipulation of generators by functions
    """
    def __init__(self, function, obj, *args, **kwargs):
        self.obj = obj
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def generate_raw(self, dataset=None):
        """
        Implementation of the generate_raw() method from BaseDammy. Generate a value and call the function
        using the generated value as a parameter
        """
        return self.function(self.obj.generate(dataset), *self.args, **self.kwargs)

class AttributeGetter(BaseDammy):
    """
    Allows getting attribute values from values generated by generators
    """

    def __init__(self, obj, attr):
        super(AttributeGetter, self).__init__(obj._sql_equivalent)
        self.obj = obj
        self.attr = attr

    def generate_raw(self, dataset=None):
        """
        Implementation of the generate_raw() method from BaseDammy. Generate a value and get the
        specified attribute
        """
        return getattr(self.obj.generate(dataset), self.attr)

    def __call__(self, *args, **kwargs):
        """
        Call the method with the given arguments
        """
        return MethodCaller(self.obj, self.attr, args)

class MethodCaller(BaseDammy):
    """
    Allows calling methods of values generated by generators
    """
    def __init__(self, obj, method, *args, **kwargs):
        super(MethodCaller, self).__init__(obj._sql_equivalent)
        self.obj = obj
        self.method = method
        self.args = args[0]
        self.kwargs = kwargs

    def generate_raw(self, dataset=None):
        """
        Implementation of the generate_raw() method from BaseDammy. Generate a value and call the
        specified method
        """
        method = getattr(self.obj.generate(dataset), self.method)

        if len(self.args) == 1 and len(self.args[0]) == 0:
            if len(self.kwargs) == 0:
                return method()
            else:
                return method(**self.kwargs)
        else:
            if len(self.kwargs) == 0:
                return method(*self.args)
            else:
                return method(*self.args, **self.kwargs)

class DammyGenerator(BaseDammy):
    """
    Allows addition/substraction and many other operations with regular and Dammy objects
    and it is returned when any of such operations is performed
    """
    def __init__(self, a, b, op, sql):
        super(DammyGenerator, self).__init__(sql)
        self.operator = op
        self.d1 = a
        self.d2 = b

    def generate_raw(self, dataset=None):
        """
        Implementation of the generate_raw() method from BaseDammy. Generates a value and performs the operation
        """
        if isinstance(self.d1, DammyGenerator):
            d1 = self.d1.generate_raw(dataset)

        elif isinstance(self.d1, BaseDammy):
            if self.d1._last_generated is None:
                d1 = self.d1.generate_raw(dataset)
            else:
                d1 = self.d1._last_generated
        else:
            d1 = self.d1

        if isinstance(self.d2, DammyGenerator):
            d2 = self.d2.generate_raw(dataset)

        elif isinstance(self.d2, BaseDammy):
            if self.d2._last_generated is None:
                d2 = self.d2.generate_raw(dataset)
            else:
                d2 = self.d2._last_generated
        else:
            d2 = self.d2

        if self.operator == '+':
            return self._generate(d1 + d2)
        elif self.operator == '-':
            return self._generate(d1 - d2)
        elif self.operator == '*':
            return self._generate(d1 * d2)
        elif self.operator == '/':
            return self._generate(d1 / d2)
        else:
            raise TypeError('Unknown operator {}'.format(self.operator))

############################         Database        ############################
class AutoIncrement(BaseDammy):
    """
    Represents an automatically incrementing field. By default starts by 1 and increments by 1
    """

    def __init__(self, start=1, increment=1):
        super(AutoIncrement, self).__init__('INTEGER')
        if self._last_generated is None:
            self._last_generated = start - 1
        self._increment = increment

    def generate_raw(self, dataset=None):
        """
        Implementation of the generate_raw() method from BaseDammy. Generates and updates the next value
        """
        return self._generate(self._last_generated + 1)

class DatabaseConstraint:
    """
    All database constraints must inherit from this class
    """
    def __init__(self, prefix):
        self._prefix = prefix   # Prefix currently not in use

class PrimaryKey(DatabaseConstraint):
    """
    Represents a primary key. Every field encapsulated by this class becomes a member of the primary key
    """
    def __init__(self, k):
        self.field = k
        self._sql_equivalent = k._sql_equivalent

class ForeignKey(DatabaseConstraint):
    """
    Represents a foreign key. The first parameter is the class where the referenced field is
    and the second a list of strings, each of them containing the name of a field forming
    the primary key. If any of the fields is not a member of the primary key, a IntegrityException is raised
    """
    def __init__(self, ref_table, *args):
        super(ForeignKey, self).__init__('fk')

        for attr in args:
            attr_val = getattr(ref_table, attr)
            if not isinstance(attr_val, PrimaryKey):
                raise IntegrityException('Expected PrimaryKey, got {}'.format(attr_val.__class__.__name__))

        self.ref_table = ref_table
        self.ref_fields = args

        self.table_name = ref_table.__name__

    def __len__(self):
        """
        Gets the size of the key
        """
        return len(self.ref_fields)

    def get_reference(self, dataset):
        """
        Generates a tuple of values existing in the dataset
        """
        if self.table_name in dataset.data:
            values = dataset[self.table_name]
            rand_row = random.choice(values)
            ref = tuple(rand_row[v] for v in self.ref_fields)
            return ref
        else:
            raise IntegrityException('Reference to {} not found'.format(self.table_name))