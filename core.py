import random

class DammyException(Exception):
    pass

class BaseDammy:

    _last_generated = None

    def generate(self):
        raise DammyException('The generate() method must be overridden')

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
                result[attr] = attr_obj.generate()

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
        table_columns = dict((n, c().attrs) for n, c in self._name_class_map.items())
        if create_tables:
            raise NotImplementedError("Column data types and constraints missing")
            for name, columns in table_columns.items():
                columns_with_specs = ['\t{}'.format(column) for column in columns]
                lines.append('CREATE TABLE IF NOT EXISTS "{}" (\n{}\n);'.format(name, ',\n'.join(columns_with_specs)))

        for table_name, rows in self.data.items():
            tuples = [', '.join(['"{}"'.format(value) if isinstance(value, str) else str(value) for value in row.values()]) for row in rows]
            lines.append('INSERT INTO {} ({}) VALUES \n{};'.format(table_name, ', '.join(table_columns[table_name]), ',\n'.join(['\t({})'.format(tp) for tp in tuples])))

        if save_to is None:
            return '\n'.join(lines)
        else:
            pass

    def __str__(self):
        return str(self.data)

    def __getitem__(self, key):
        return self.data[key]