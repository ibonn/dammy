"""
This module contains the DatasetGenerator class. This class generates a set of
different types of entities related to each other, and is useful to generate
entire databases, where each table is linked to another one by a foreign key.

It can also be used in NoSQL databases.
"""
from .core import ForeignKey, PrimaryKey, BaseDammy

############################    HELPER FUNCTIONS    ############################
def infer_type(o):
    """
    Tries to infer the SQL equivalent data type
    o -> The object from which the type will be inferred
    returns a string with the equivalent SQL type
    raises a TypeError if no equivalent type is found
    """
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
    """
    Tries to convert a python literal to its SQL equivalent
    o -> the literal object to ve converted
    returns the given object converted to a SQL literal
    """
    if isinstance(o, str):
        return '"{}"'.format(o)
    else:
        return str(o)

class DatasetGenerator:
    """
    This class generates a set of
    different types of entities related to each other, and is useful to generate
    entire databases, where each table is linked to another one by a foreign key.

    It can also be used in NoSQL databases.
    """
    def __init__(self, *kwargs):
        self.data = {}
        self._counters = dict((v[0].__name__, v[1]) for v in kwargs)
        self._name_class_map = dict((v[0].__name__, v[0]) for v in kwargs)

        for c, n in kwargs:
            if self._counters[c.__name__] != 0:
                for i in range(0, n):
                    self._generate_entity(c.__name__)

    def _generate_entity(self, c):
        """
        Generates a single entity of the given class
        """
        if c in self.data:
            self.data[c].append(self._name_class_map[c]().generate(self))
            self._counters[c] -= 1
        else:
            self.data[c] = []
            self._generate_entity(c)

    def get_sql(self, save_to=None, create_tables=True):
        """
        Gets the dataset as SQL INSERT statements. The generated SQL is always returned and if save_to is specified,
        it is saved to that location. Additional CREATE TABLE statements are added if create_tables is set to True
        """
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
        """
        Counts the number of tables
        """
        return len(self.data)

    def __str__(self):
        """
        Get all the data as a string
        """
        return str(self.data)

    def __getitem__(self, key):
        """
        Gets the content of a specific table as a dict
        """
        return self.data[key]