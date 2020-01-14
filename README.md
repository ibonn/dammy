![GitHub top language](https://img.shields.io/github/languages/top/ibonn/dammy)
![Travis (.org)](https://img.shields.io/travis/ibonn/dammy)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c321b2ee18234712aff9ce2ca69ae6eb)](https://www.codacy.com/manual/ibonn/dammy?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ibonn/dammy&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/141299ec4d7519f889d6/maintainability)](https://codeclimate.com/github/ibonn/dammy/maintainability)
[![PyPI download month](https://img.shields.io/pypi/dm/dammy.svg)](https://pypi.python.org/pypi/dammy/)
[![PyPI download week](https://img.shields.io/pypi/dw/dammy.svg)](https://pypi.python.org/pypi/dammy/)
[![PyPI download day](https://img.shields.io/pypi/dd/dammy.svg)](https://pypi.python.org/pypi/dammy/)

# dammy

Populate your database with dummy data
## Table of contents

* [Introduction](#introduction)
* [Features](#features)
* [Example](#example)
* [Installation](#installation)
* [Release history](#release-history)

## Introduction

With dammy you can populate your database with a few lines of code.

## Features
* A set of prebuilt objects (Person names, country names, car manufacturers and models, random dates...)
* The possibility to expand the previous library
* Generate datasets and export them to SQL

## Example

If you wanted to generate 1000 random people, just define what a person looks like and dammy will handle the rest

``` python
from dammy import DammyEntity
from dammy.stdlib import RandomName, RandomString, RandomDateTime, RandomInteger, CountryName

class Person(DammyEntity):
    first_name = RandomName()
    password = RandomString(5)
    birthday = RandomDateTime(start=datetime(1980, 1, 1), end=datetime(2000, 12, 31), date_format='%d/%m/%Y')
    favorite_number = RandomInteger(0, 10)
    age = datetime.now() - birthday
    country = CountryName()

# Generate 1000 random people
for i in range(0, 1000):
    print(Person())
```

It also supports relationships between tables
``` python
from dammy import DammyEntity
from dammy.db import AutoIncrement, PrimaryKey, ForeignKey
from dammy.stdlib import RandomName, RandomString, RandomDateTime, RandomInteger, CountryName

# Define what a person looks like
class Person(DammyEntity):
    identifier = PrimaryKey(AutoIncrement())
    first_name = RandomName()
    password = RandomString(5)
    birthday = RandomDateTime(start=datetime(1980, 1, 1), end=datetime(2000, 12, 31), date_format='%d/%m/%Y')
    favorite_number = RandomInteger(0, 10)
    age = datetime.now() - birthday
    country = CountryName()

# Define what a car looks like
class Car(DammyEntity):
    identifier = PrimaryKey(AutoIncrement())
    manufacturer_name = CarBrand())
    model = CarModel(car_brand=manufacturer_name)
    owner = ForeignKey(Person, 'identifier')
```

And data can be exported to SQL
``` python
from dammy import DatasetGenerator

# Generate a dataset with 20000 cars and 94234 people
dataset = DatasetGenerator((Car, 20000), (Person, 94234))
dataset.get_sql(save_to='cars_with_owners.sql')
```
## Installation
To install the latest release of dammy pip run
```
pip install dammy
```

## Release history
* 0.0.3
    * Fixed import bug in stdlib
* 0.0.1
    * First release
