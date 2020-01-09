import random

class DammyException(Exception):
    pass

def get_reference(value, dataset):
    if value.references_table.__name__ in dataset.data:
        values = dataset[value.references_table.__name__]
        return random.choice(values)[value.references_field]
    else:
        raise DammyException('Reference to {} not found'.format(value.references_table.__name__))

def infer_type(element):
    if isinstance(element, bool):
        return 'BOOLEAN'
    elif isinstance(element, str):
        return 'VARCHAR'
    elif isinstance(element, int):
        return 'INTEGER'

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

class MultiValuedDammy(BaseDammy):
    def __init__(self, *args):
        self._values = args

    def generate(self):
        return [value.generate() for value in self._values]

class DammyEntity(BaseDammy):
    def __init__(self):
        self.attrs = [i for i, v in self.__class__.__dict__.items() if i[:1] != '_' and not callable(v)]

    def generate(self, dataset=None):
        result = {}
        for attr in self.attrs:
            attr_obj = getattr(self, attr)
            if isinstance(attr_obj, ForeignKey):
                if dataset is None:
                    raise DammyException('Reference to an entity ({}) given but no dataset containing {}s supplied'.format(attr_obj.references_table.__name__, attr_obj.references_table.__name__))
                else:
                    if isinstance(dataset, DatasetGenerator):
                        while dataset._counters[attr_obj.references_table.__name__] != 0:
                            dataset._generate_entity(attr_obj.references_table.__name__)

                    chosen = random.choice(dataset[attr_obj.references_table.__name__])
                    result[attr] = chosen[attr_obj.references_field]
            elif isinstance(attr_obj, BaseDammy):
                result[attr] = attr_obj.generate(dataset)
            else:
                result[attr] = attr_obj

        return result

    def __iter__(self):
        for x in self.generate().items():
            yield x

    def __str__(self):
        return str(dict(self))

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


    def get_sql(self, create_tables=True, save_to=None):
        lines = []
        tables_columns_types = {} 
        tables_constraints = {}
        table_order = []
        for n, c in self._name_class_map.items():
            tables_constraints[n] = []
            d = {}
            instance = c()
            for attr in instance.attrs:
                o = getattr(instance, attr)
                if isinstance(o, ForeignKey):
                    ref = o.references_table()
                    d[attr] = getattr(ref, o.references_field)._sql_equivalent
                    if o.references_table.__name__ not in table_order:
                        table_order.append(o.references_table.__name__)
                    # table_order.add(n)
                    tables_constraints[n].append('CONSTRAINT fk_{}_{} FOREIGN KEY ({}) REFERENCES {}({})'.format(n, o.references_table.__name__, attr, o.references_table.__name__, o.references_field))
                elif isinstance(o, BaseDammy):
                    d[attr] = o._sql_equivalent
                else:
                    d[attr] = infer_type(o)

            if n not in table_order:
                table_order.append(n)
            tables_columns_types[n] = d

        if create_tables:
            for table_name in table_order:
                columns_with_specs = ['\t{} {}'.format(column, t) for column, t in tables_columns_types[table_name].items()]
                constraints = ['\t{}'.format(constraint) for constraint in tables_constraints[table_name]]
                lines.append('CREATE TABLE IF NOT EXISTS "{}" (\n{}\n);'.format(table_name, ',\n'.join(columns_with_specs + constraints)))

        for table_name in table_order:
            tuples = [', '.join(['"{}"'.format(value) if isinstance(value, str) else str(value) for value in row.values()]) for row in self.data[table_name]]
            lines.append('INSERT INTO {} ({}) VALUES \n{};'.format(table_name, ', '.join(tables_columns_types[table_name].keys()), ',\n'.join(['\t({})'.format(tp) for tp in tuples])))

        sql = '\n'.join(lines)

        if save_to is not None:
            with open(save_to, 'w') as f:
                f.write(sql)
        return sql  

    def __str__(self):
        return str(self.data)

    def __getitem__(self, key):
        return self.data[key]

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
    pass    # TODO

class Constraint(DatabaseConstraint):
    pass    # TODO

class Unique(DatabaseConstraint):
    pass    # TODO

class NotNull(DatabaseConstraint):
    pass    # TODO

class PrimaryKey(DatabaseConstraint):
    pass    # TODO

class ForeignKey(DatabaseConstraint):
    def __init__(self, references_table, references_field):
        self.references_table = references_table
        self.references_field = references_field

class Check(DatabaseConstraint):
    pass    # TODO

class Default(DatabaseConstraint):
    pass    # TODO

class Index(DatabaseConstraint):
    pass    # TODO