import random

"""
    HELPER FUNCTIONS
"""
def infer_type(o):
    if isinstance(o, bool):
        return 'BOOLEAN'
    elif isinstance(o, int):
        return 'INTEGER'
    elif isinstance(o, float):
        return 'FLOAT'
    elif isinstance(o, str):
        return 'VARCHAR({})'.format(len(o))
    else:
        raise TypeError('Type {} has not SQL equivalent'.format(type(o)))

def sql_literal(o):
    if isinstance(o, str):
        return '"{}"'.format(o)
    else:
        return str(o)

"""
    EXCEPTIONS
"""
class DammyException(Exception):
    pass

"""
    BASE CLASSES
"""
class BaseDammy:

    def __init__(self, sql_equivalent):
        self._last_generated = None
        self._sql_equivalent = sql_equivalent

    def generate_raw(self, dataset=None):
        raise DammyException('The generate_raw() method must be overridden')

    def generate(self, dataset=None):
        return self.generate_raw(dataset)

    def _generate(self, value):
        self._last_generated = value
        return value

    # +
    def __add__(self, other):
        return DammyGenerator(self, other, '+', self._sql_equivalent)

    # -
    def __sub__(self, other):
        return DammyGenerator(self, other, '-', self._sql_equivalent)

    # *
    def __mul__(self, other):
        return DammyGenerator(self, other, '*', self._sql_equivalent)

    # %
    def __mod__(self, other):
        raise NotImplementedError()

    # //
    def __div__(self, other):
        raise NotImplementedError()

    # /
    def __truediv__(self, other):
        return DammyGenerator(self, other, '/', self._sql_equivalent)

    # <
    def __lt__(self, other):
        raise NotImplementedError()

    # <=
    def __le__(self, other):
        raise NotImplementedError()

    # ==
    def __eq__(self, other):
        raise NotImplementedError()

    # !=
    def __ne__(self, other):
        raise NotImplementedError()

    # >
    def __gt__(self, other):
        raise NotImplementedError()

    # >=
    def __ge__(self, other):
        raise NotImplementedError()

    def __str__(self):
        return self.generate()

    def __getattr__(self, name):
        return AttributeGetter(self, name)

class DammyEntity(BaseDammy):
    def __init__(self):
        items = self.__class__.__dict__.items()
        self.attrs = [i for i, v in items if i[:1] != '_' and not callable(v)]
        self.primary_key = [i for i, v in items if isinstance(v, PrimaryKey)]
        self.foreign_keys = [i for i, v in items if isinstance(v, ForeignKey)]


    def generate_raw(self, dataset=None):
        result = {}
        for attr in self.attrs:
            attr_obj = getattr(self, attr)

            # Get references to foreign keys
            if isinstance(attr_obj, ForeignKey):
                if dataset is None:
                    raise DammyException(
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

    def __iter__(self):
        for x in self.generate().items():
            yield x

    def __str__(self):
        return str(self.generate())

class AttributeGetter(BaseDammy):
    def __init__(self, obj, attr):
        super(AttributeGetter, self).__init__(obj._sql_equivalent)
        self.obj = obj
        self.attr = attr

    def generate_raw(self, dataset=None):
        return getattr(self.obj.generate(dataset), self.attr)

    def __call__(self, *args, **kwargs):
        return MethodCaller(self.obj, self.attr, args)

class MethodCaller(BaseDammy):
    def __init__(self, obj, method, *args, **kwargs):
        super(MethodCaller, self).__init__(obj._sql_equivalent)
        self.obj = obj
        self.method = method
        self.args = args[0]
        self.kwargs = kwargs

    def generate_raw(self, dataset=None):
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
    This class is not intended for regular usage.
    It is used to allow addition/substraction...
    operations with regular and Dammy objects
    and it is returned when such operation is performed
    """
    def __init__(self, a, b, op, sql):
        super(DammyGenerator, self).__init__(sql)
        self.operator = op
        self.d1 = a
        self.d2 = b

    def generate_raw(self, dataset=None):
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

"""
    DATASET
"""
class DatasetGenerator:
    def __init__(self, *kwargs):
        self.data = {}
        self._counters = dict((v[0].__name__, v[1]) for v in kwargs)
        self._name_class_map = dict((v[0].__name__, v[0]) for v in kwargs)

        for c, n in kwargs:
            if self._counters[c.__name__] != 0:
                for i in range(0, n):
                    self._generate_entity(c.__name__)

    def _generate_entity(self, c):
        if c in self.data:
            self.data[c].append(self._name_class_map[c]().generate(self))
            self._counters[c] -= 1
        else:
            self.data[c] = []
            self._generate_entity(c)

    def get_sql(self, save_to=None, create_tables=True):
        table_order = []
        tables = {}
        instances = {}
        for name, c in self._name_class_map.items():

            tables[name] = {
                'columns': [],
                'column_types': [],
                'constraints': []
            }

            instances[name] = c()

            tables[name]['constraints'].append(
                'CONSTRAINT pk_{} PRIMARY KEY ({})'.format(
                    name,
                    ', '.join(instances[name].primary_key)
                    )
                )

            for col in instances[name].attrs:
                col_obj = getattr(instances[name], col)

                if isinstance(col_obj, ForeignKey):
                    fk_fields = []

                    for field in col_obj.ref_fields:
                        ref_field = getattr(col_obj.ref_table, field)
                        fk_fields.append('{}_{}'.format(col, field))
                        tables[name]['column_types'].append(ref_field._sql_equivalent)

                    tables[name]['columns'].extend(fk_fields)

                    tables[name]['constraints'].append(
                        'CONSTRAINT fk_{} ({}) REFERENCES {}({})'.format(
                            col,
                            ', '.join(fk_fields),
                            col_obj.table_name,
                            ', '.join(col_obj.ref_fields)
                        )
                    )

                    if col_obj.table_name not in table_order:
                        table_order.append(col_obj.table_name)

                elif isinstance(col_obj, PrimaryKey):
                    tables[name]['columns'].append(col)
                    tables[name]['column_types'].append(col_obj.field._sql_equivalent)

                elif isinstance(col_obj, BaseDammy):
                    tables[name]['columns'].append(col)
                    tables[name]['column_types'].append(col_obj._sql_equivalent)

                else:
                    tables[name]['columns'].append(col)
                    tables[name]['column_types'].append(infer_type(col))

            if name not in table_order:
                table_order.append(name)

        lines = []

        if create_tables:
            for table in table_order:
                lines.append(
                    'CREATE TABLE IF NOT EXISTS {} (\n\t{}\n);'.format(
                        table,
                        ',\n\t'.join([' '.join(x) for x in zip(tables[table]['columns'], tables[table]['column_types'])] + tables[table]['constraints'])
                    )
                )
        
        for table in table_order:
            for row in self.data[table]:
                lines.append(
                    'INSERT INTO {} ({}) VALUES ({});'.format(
                        table,
                        ', '.join(tables[table]['columns']),
                        ', '.join([sql_literal(x) for x in row.values()]),
                    )
                )

        sql = '\n'.join(lines)

        if save_to is not None:
            with open(save_to, 'w') as f:
                f.write(sql)

        return sql

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def __getitem__(self, key):
        return self.data[key]

"""
    DATABASE
"""
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
        Generates and updates the next value
        """
        return self._generate(self._last_generated + 1)

class DatabaseConstraint:
    def __init__(self, prefix):
        self._prefix = prefix

class PrimaryKey(DatabaseConstraint):
    def __init__(self, k):
        self.field = k
        self._sql_equivalent = k._sql_equivalent

class ForeignKey(DatabaseConstraint):
    def __init__(self, ref_table, *args):
        super(ForeignKey, self).__init__('fk')

        for attr in args:
            attr_val = getattr(ref_table, attr)
            if not isinstance(attr_val, PrimaryKey):
                raise Exception('Expected PrimaryKey, got {}'.format(attr_val.__class__.__name__))

        self.ref_table = ref_table
        self.ref_fields = args

        self.table_name = ref_table.__name__

    def __len__(self):
        return len(self.ref_fields)

    def get_reference(self, dataset):
        if self.table_name in dataset.data:
            values = dataset[self.table_name]
            rand_row = random.choice(values)
            ref = tuple(rand_row[v] for v in self.ref_fields)
            return ref
        else:
            raise DammyException('Reference to {} not found'.format(self.table_name))