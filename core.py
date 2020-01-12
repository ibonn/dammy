import random

# TODO
def infer_type(o):
    if isinstance(o, bool):
        return 'BOOLEAN'
    if isinstance(o, int):
        return 'INTEGER'
    else:
        raise TypeError('Type {} has not SQL equivalent'.format(type(o)))

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

    def generate(self, dataset=None):
        raise DammyException('The generate() method must be overridden')

    def _generate(self, value):
        self._last_generated = value
        return value

    def __add__(self, other):
        return MultiValuedDammy(self, other)

    def __str__(self):
        return self.generate()

    # def __getattr__(self, name):
    #     pass

class MultiValuedDammy(BaseDammy):
    def __init__(self, *args):
        self._values = args

    def generate(self):
        return [value.generate() for value in self._values]

class DammyEntity(BaseDammy):
    def __init__(self):
        items = self.__class__.__dict__.items()
        self.attrs = [i for i, v in items if i[:1] != '_' and not callable(v)]
        self.primary_key = [i for i, v in items if isinstance(v, PrimaryKey)]
        self.foreign_keys = [i for i, v in items if isinstance(v, ForeignKey)]

    def generate(self, dataset=None):
        result = {}
        for attr in self.attrs:
            attr_obj = getattr(self, attr)

            # Get references to foreign keys
            if isinstance(attr_obj, ForeignKey):
                if dataset is None:
                    raise DammyException('Reference to an entity ({}) given but no dataset containing {}s supplied'.format(attr_obj.references_table.__name__, attr_obj.references_table.__name__))
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
        return str(dict(self))

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

    def generate(self, dataset=None):
        if isinstance(self.d1, BaseDammy):
            d1 = self.d1.generate()
        else:
            d1 = self.d1

        if isinstance(self.d2, BaseDammy):
            d2 = self.d2.generate()
        else:
            d2 = self.d2

        if self.operator == '+':
            return self._generate(d1 + d2)
        elif self.operator == '-':
            return self._generate(d1 - d2)
        elif self.operator == '*':
            raise NotImplementedError()
        elif self.operator == '/':
            raise NotImplementedError
        else:
            # TODO
            raise Exception()

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

        lines = []

        if create_tables:
            table_def = {}
            table_order = []
            for table, data in self.data.items():
                instance = self._name_class_map[table]()
                columns = instance.attrs
                primary_key = instance.primary_key
                foreign_keys = instance.foreign_keys

                columns_info = []
                constraint_info = []

                for attr in columns:
                    if attr in foreign_keys:
                        fk_fields = []
                        fk = getattr(self._name_class_map[table], attr)
                        for f in fk.ref_fields:
                            field = getattr(fk.ref_table, f)
                            name = '{}_{}'.format(attr, f)
                            fk_fields.append(name)
                            columns_info.append('{} {}'.format(name, field._sql_equivalent))

                        if fk.table_name not in table_order:
                            table_order.append(fk.table_name)

                        constraint_info.append('CONSTRAINT fk_{} FOREIGN KEY ({}) REFERENCES {}({})'.format(attr, ', '.join(fk_fields), fk.table_name, ', '.join(fk.ref_fields)))

                    elif attr in primary_key:
                        field = getattr(self._name_class_map[table], attr)
                        columns_info.append('{} {}'.format(attr, field.field._sql_equivalent))

                    else:
                        field = getattr(self._name_class_map[table], attr)
                        if isinstance(field, BaseDammy):
                            columns_info.append('{} {}'.format(attr, field._sql_equivalent))
                        else:
                            columns_info.append('{} {}'.format(attr, infer_type(field)))

                constraint_info.append('CONSTRAINT pk_{} PRIMARY KEY ({})'.format('_'.join(primary_key), ', '.join(primary_key)))
                table_info = columns_info + constraint_info

                if table not in table_order:
                    table_order.append(table)
                table_def[table] = 'CREATE TABLE IF NOT EXISTS {} (\n\t{}\n);'.format(table, ',\n\t'.join(table_info))

            for table in table_order:
                lines.append(table_def[table])

        for table, data in self.data.items():
            columns = self._name_class_map[table]().attrs
            table_data =',\n\t'.join(['({})'.format(', '.join(['"{}"'.format(v) if isinstance(v, str) else str(v) for v in row.values()])) for row in data])
            lines.append('INSERT INTO {} ({}) VALUES \n\t{};'.format(table, ', '.join(columns), table_data))

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

    """
    Generates and updates the next value
    """
    def generate(self, dataset=None):
        return self._generate(self._last_generated + 1)

class DatabaseConstraint:
    def __init__(self, prefix):
        self._prefix = prefix

    def _get_sql(self, *args):
        raise NotImplementedError('The _get_sql() method must be overridden')

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
                raise Exception('Expected PrimaryKey or Unique, got {}'.format(attr_val.__class__.__name__))
        
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