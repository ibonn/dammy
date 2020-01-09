import random

class DammyException(Exception):
    pass

def contains_reference(value):
    return '__' in value

def get_reference(value, dataset):
    parts = value.split('__')
    if parts[0] in dataset.data:
        values = dataset[parts[0]]
        return random.choice(values)[parts[1]]
    else:
        raise DammyException('Reference to {} not found'.format(parts[0]))

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
            if isinstance(attr_obj, str):
                parts = attr_obj.split('__')
                if dataset is None:
                    raise DammyException('Reference to an entity ({}) given but no dataset containing {}s supplied'.format(parts[0], parts[0]))
                else:
                    if isinstance(dataset, DatasetGenerator):
                        while dataset._counters[parts[0]] != 0:
                            dataset._generate_entity(parts[0])

                    chosen = random.choice(dataset[parts[0]])
                    result[attr] = chosen[parts[1]]
            else:
                result[attr] = attr_obj.generate(dataset)

        return result
        # return dict((attr, getattr(self, attr).generate()) for attr in self.attrs)

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
        for n, c in self._name_class_map.items():
            tables_constraints[n] = []
            d = {}
            instance = c()
            for attr in instance.attrs:
                o = getattr(instance, attr)
                if isinstance(o, str):
                    parts = o.split('__')
                    ref = self._name_class_map[parts[0]]()
                    d[attr] = getattr(ref, parts[1])._sql_equivalent
                    tables_constraints[n].append('CONSTRAINT fk_{}_{} FOREIGN KEY ({}) REFERENCES {}({})'.format(n, parts[0], attr, parts[0], parts[1]))
                else:
                    d[attr] = o._sql_equivalent
            tables_columns_types[n] = d

        if create_tables:
            #raise NotImplementedError("Column data types and constraints missing")
            for name, columns in tables_columns_types.items():
                columns_with_specs = ['\t{} {}'.format(column, t) for column, t in columns.items()]
                constraints = ['\t{}'.format(constraint) for constraint in tables_constraints[name]]
                lines.append('CREATE TABLE IF NOT EXISTS "{}" (\n{}\n);'.format(name, ',\n'.join(columns_with_specs + constraints)))

        for table_name, rows in self.data.items():
            tuples = [', '.join(['"{}"'.format(value) if isinstance(value, str) else str(value) for value in row.values()]) for row in rows]
            lines.append('INSERT INTO {} ({}) VALUES \n{};'.format(table_name, ', '.join(tables_columns_types[table_name].keys()), ',\n'.join(['\t({})'.format(tp) for tp in tuples])))

        if save_to is None:
            return '\n'.join(lines)
        else:
            pass

    def __str__(self):
        return str(self.data)

    def __getitem__(self, key):
        return self.data[key]