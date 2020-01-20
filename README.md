# dammy

![GitHub top language](https://img.shields.io/github/languages/top/ibonn/dammy)
[![Documentation Status](https://readthedocs.org/projects/dammy/badge/?version=latest)](https://dammy.readthedocs.io/en/latest/?badge=latest)
![Travis (.org)](https://img.shields.io/travis/ibonn/dammy)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c321b2ee18234712aff9ce2ca69ae6eb)](https://www.codacy.com/manual/ibonn/dammy?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ibonn/dammy&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/141299ec4d7519f889d6/maintainability)](https://codeclimate.com/github/ibonn/dammy/maintainability)
[![PyPI download month](https://img.shields.io/pypi/dm/dammy.svg)](https://pypi.python.org/pypi/dammy/)
[![PyPI download week](https://img.shields.io/pypi/dw/dammy.svg)](https://pypi.python.org/pypi/dammy/)
[![PyPI download day](https://img.shields.io/pypi/dd/dammy.svg)](https://pypi.python.org/pypi/dammy/)

Generate fake/dummy data for any purpose

## Table of contents

* [Introduction](#introduction)
* [Features](#features)
* [Example](#example)
* [Installation](#installation)
* [Release history](#release-history)

## Introduction

dammy is a powerful and simple tool to generate fake data. You can use it to mock classes, populate databases and and much more.
You can check the full documentation [here](https://readthedocs.org/projects/dammy/).

## Features
* Generate anything within the set of prebuilt objects (Person names, country names, car manufacturers and models, random dates...)
* Compose more complex data easily (Full profiles, complete databases, )
* The possibility to expand the previous set with little to no code
* Completely intuitive, you will learn to use it in less than 10 minutes
* Export the generated data to SQL

## Example

If you wanted to generate 1000 random people, just define what a person looks like and dammy will handle the rest

``` python
from dammy import EntityGenerator
from dammy.functions import cast
from dammy.stdlib import RandomName, RandomString, RandomDateTime, RandomInteger, CountryName

class Person(EntityGenerator):
    first_name = RandomName().upper()
    password = RandomString(5)
    birthday = RandomDateTime(start=datetime(1980, 1, 1), end=datetime(2000, 12, 31), date_format='%d/%m/%Y')
    favorite_number = RandomInteger(0, 10)
    age = cast((datetime.now() - birthday).days / 365.25, int)
    country = CountryName()

# Generate 1000 random people
for i in range(0, 1000):
    print(Person())
```

It also supports relationships between tables, so you can generate data to populate databases
``` python
from dammy import EntityGenerator
from dammy.db import AutoIncrement, PrimaryKey, ForeignKey
from dammy.stdlib import RandomName, RandomString, RandomDateTime, RandomInteger, CountryName

# Define what a person looks like
class Person(EntityGenerator):
    id_pk = PrimaryKey(id=AutoIncrement())
    first_name = RandomName().upper()
    password = RandomString(5)
    birthday = RandomDateTime(start=datetime(1980, 1, 1), end=datetime(2000, 12, 31), date_format='%d/%m/%Y')
    favorite_number = RandomInteger(0, 10)
    age = cast((datetime.now() - birthday).days / 365.25, int)
    country = CountryName()

# Define what a car looks like
class Car(EntityGenerator):
    id_pk = PrimaryKey(id=AutoIncrement())
    manufacturer_name = CarBrand()
    model = CarModel(car_brand=manufacturer_name)
    owner = ForeignKey(Person, 'identifier')
```

And the data can be exported to SQL
``` python
from dammy import DatasetGenerator

# Generate a dataset with 20000 cars and 94234 people
dataset = DatasetGenerator((Car, 20000), (Person, 94234)).generate()
dataset.get_sql(save_to='cars_with_owners.sql')
```
## Installation
To install the latest stable release of dammy using pip
```
pip install dammy
```

You can also install the latest development release by cloning the repository and installing it with pip
```
git clone https://github.com/ibonn/dammy.git dammy
cd dammy
pip install -e .
```

## Release history
* 1.0.0
    * Semantic versioning used from now on
    * Documentation fixed
    * Minor code changes (duplicated code removed...)

* 0.1.3
    * Code refactored
    * All binary operations made possible between BaseGenerator objects
    * BaseDammy renamed to BaseGenerator
    * EntityGenerator renamed to OperationResult
    * DammyEntity renamed to EntityGenerator
    * Everything inherits from BaseGenerator
    * Removed DatabaseConstraint
    * Added UNIQUE constraint support
    * Datasets can now be exported to JSON
    * Entities can now be exported to JSON and CSV
    * dammy.stdlib expanded with new built-in generators

* 0.1.2
    * Documentation improved
    * DatasetGenerator moved from main to db
    * Minor bugs fixed

* 0.1.1
    * Can get attributes of entities
    * Can call methods on entities
    * Ability to perform operations added
    * Code improved
    * Docstrings added

* 0.0.3
    * Fixed import bug in stdlib

* 0.0.1
    * First release