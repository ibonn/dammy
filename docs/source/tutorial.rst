.. _tutorial:

Tutorial
**************************
Welcome to the tutorial section! Here you will learn to use dammy to its fullest
following an example that will grow each step, starting at the simplest and ending
using all the functionalities available.

In this example wie will build a dataset containing persons and cars, each person being
the owner of at least one car.

What is a generator?
====================
In dammy, a generator is a class which generates random data. Plain and simple. 
All generators must inherit :class:`dammy.BaseDammy`. Generators can be simple or
composite. A simple generator generates a value, while a composite generator is composed
of multiple simple generators and generates a value for each of them.

For example, a integer generator is a simple generator, because it only generates integers.
A person generator is composite because generates a name, an age, a height...

In our example, we will need 2 composite generators, one for the person and one for the car::

    class Person():
        # The description of a person goes here
        pass

    class Car():
        # The description of a person goes here
        pass

Composite generators must inherit from :class:`dammy.DammyEntity`. So the final code looks like this::

    from dammy import DammyEntity

    class Person(DammyEntity):
        # The description of a person goes here
        pass

    class Car(DammyEntity):
        # The description of a car goes here
        pass

Now you could instantiate these classes and call their generate() method, although it will return an empty
dictionary because they contain no attributes. We will add some attributes right now.

Built-in generators
===================
A person must have some attributes such as name, age, country of origin... and a car should have
a brand, a model and a plate number.

But how to generate all of this? Don't worry about it, we have taken care of it and done the hard work
for you. To generate all of this, just import stdlib (:doc:`stdlib`) and add the generators as follows::

    from dammy import DammyEntity
    from dammy.stdlib import RandomName, CountryName, RandomInteger, CarBrand, CarModel

    class Person(DammyEntity):
        name = RandomName()         # Generate a random name (any gender)
        age = RandomInteger(18, 99) # Generate a randim integer between 18 and 99
        country = CountryName()     # Generate a country name

    class Car(DammyEntity):
        brand = CarBrand()                  # Generate a car brand
        model = CarModel(car_brand=brand)   # Generate a car model matching that brand
        plate = RandomInteger(1000, 9999)   # Generate a plate number

You can check all the available generators at :doc:`stdlib`

.. note::
    Note that the car brand can be passed as a parameter on CarModel to generate car models corresponding to the
    generated manufacturer.

With this, you can already generate individual cars and people! Just run::

    print(Car())
    print(Person())

And you will get the following output::

    >>> print(Car())
    {'brand': 'Kia', 'model': 'Cadenza', 'plate': 9138}
    >>> print(Person())
    {'name': 'Meir', 'age': 35, 'country': 'Switzerland'}

.. note::
    Keep in mind that you don't have to create an instance every time you want to generate a new entity. The example above
    prints a new entity because the __str__() method calls the .generate() method.

    In other words, you can also generate a car and a person like this::

        c = Car()
        c.generate()

Playing with generators
=======================
Now, lets suppose we want a person to have a field called birthdate, which obviously contains the persons birth date.
We also want the car model name to be uppercase. How do we make the birthdate date match the age?
And how can we alter the generated values if we cant access them until they are generated?

It is quite easy if you already know how to do all of this in python. You want to convert a string to uppercase, just call the .upper() method on the string.
Want to get someones age? Get the current date and the birthdate and substract them. 

With dammy it's just the same. If you are generating a string, you can call any methods, access any attributes and use all the operators of the string class.
This principle extends to every dammy entity, no matter the type of the generated value.

The updated example looks like this::

    from datetime import datetime

    from dammy import DammyEntity
    from dammy.functions import cast
    from dammy.stdlib import RandomName, CountryName, RandomInteger, CarBrand, CarModel, RandomDateTime

    class Person(DammyEntity):
        name = RandomName()         # Generate a random name (any gender)
        birthdate = RandomDateTime(start=datetime(1980, 1, 1), end=datetime(2000, 12, 31), date_format='%d/%m/%Y')  # Generate a random datetime
        age = cast((datetime.now() - birthdate).days / 365.25, int) # Get the difference in days, divide it by 365.25 to get it in years and cast it to an integer
        country = CountryName()     # Generate a country name

    class Car(DammyEntity):
        brand = CarBrand()                          # Generate a car brand
        model = CarModel(car_brand=brand).upper()   # Generate a car model matching that brand and convert it to uppercase
        plate = RandomInteger(1000, 9999)           # Generate a plate number

Note that some new imports are required

Now if you generate a car and a person as we did before you will get the following::

    >>> print(Car())
    {'brand': 'Opel', 'model': 'MERIVA', 'plate': 8130}
    >>> print(Person())
    {'name': 'Brianny', 'birthdate': '16/04/1991', 'age': 28, 'country': 'Guyana'}

Generating a a dataset
======================
To generate a dataset, persons and cars must be linked in some way. You could just do this::

    from datetime import datetime

    from dammy import DammyEntity
    from dammy.functions import cast
    from dammy.stdlib import RandomName, CountryName, RandomInteger, CarBrand, CarModel, RandomDateTime

    class Person(DammyEntity):
        name = RandomName()         # Generate a random name (any gender)
        birthdate = RandomDateTime(start=datetime(1980, 1, 1), end=datetime(2000, 12, 31), date_format='%d/%m/%Y')  # Generate a random datetime
        age = cast((datetime.now() - birthdate).days / 365.25, int) # Get the difference in days, divide it by 365.25 to get it in years and cast it to an integer
        country = CountryName()     # Generate a country name

    class Car(DammyEntity):
        brand = CarBrand()                          # Generate a car brand
        model = CarModel(car_brand=brand).upper()   # Generate a car model matching that brand and convert it to uppercase
        plate = RandomInteger(1000, 9999)           # Generate a plate number
        owner = Person()                            # Generate a person

And just generating a new car would generate a person associated to that car::

    >>> print(Car())
    {'brand': 'Ford', 'model': 'KA', 'plate': 7970, 'owner': {'name': 'Ayat', 'birthdate': '27/12/1981', 'age': 38, 'country': 'Bermuda'}}

But this way one to one relationships can only be established, and does not work very well when working with relational databases.

Primary and foreign keys can be used to achive this, as you would do with a regular database::

    from datetime import datetime

    from dammy import DammyEntity
    from dammy.db import PrimaryKey, ForeignKey, AutoIncrement
    from dammy.functions import cast
    from dammy.stdlib import RandomName, CountryName, RandomInteger, CarBrand, CarModel, RandomDateTime

    class Person(DammyEntity):
        identifier = PrimaryKey(AutoIncrement())    # Add an autoincrement and make it primary key
        name = RandomName()         # Generate a random name (any gender)
        birthdate = RandomDateTime(start=datetime(1980, 1, 1), end=datetime(2000, 12, 31), date_format='%d/%m/%Y')  # Generate a random datetime
        age = cast((datetime.now() - birthdate).days / 365.25, int) # Get the difference in days, divide it by 365.25 to get it in years and cast it to an integer
        country = CountryName()     # Generate a country name

    class Car(DammyEntity):
        brand = CarBrand()                          # Generate a car brand
        model = CarModel(car_brand=brand).upper()   # Generate a car model matching that brand and convert it to uppercase
        plate = RandomInteger(1000, 9999)           # Generate a plate number
        owner = ForeignKey(Person, 'identifier')    # Reference to an existing person

Notice once again that new imports have been added

.. warning::
    Generating a Car now requires a dataset containing persons to be passed when calling the generate() method.
    If a dataset is not present a :class:`dammy.exception.DatasetRequiredException` will be raised.

    In fact, it is not recommended to generate entities this way when they contain references.
    The safest way is using a :class:`dammy.db.DatasetGenerator`.

    

To generate a car, now we need a dataset containing persons. The dataset can be a dictionary or a :class:`dammy.db.DatasetGenerator`
But now cars contain references to people, so the best way to generate them is generating a dataset containing cars and people. This
can be done using :class:`dammy.db.DatasetGenerator`::

    from datetime import datetime

    from dammy import DammyEntity
    from dammy.db import PrimaryKey, ForeignKey, AutoIncrement, DatasetGenerator
    from dammy.functions import cast
    from dammy.stdlib import RandomName, CountryName, RandomInteger, CarBrand, CarModel, RandomDateTime

    class Person(DammyEntity):
        identifier = PrimaryKey(AutoIncrement())    # Add an autoincrement and make it primary key
        name = RandomName()         # Generate a random name (any gender)
        birthdate = RandomDateTime(start=datetime(1980, 1, 1), end=datetime(2000, 12, 31), date_format='%d/%m/%Y')  # Generate a random datetime
        age = cast((datetime.now() - birthdate).days / 365.25, int) # Get the difference in days, divide it by 365.25 to get it in years and cast it to an integer
        country = CountryName()     # Generate a country name

    class Car(DammyEntity):
        brand = CarBrand()                          # Generate a car brand
        model = CarModel(car_brand=brand).upper()   # Generate a car model matching that brand and convert it to uppercase
        plate = RandomInteger(1000, 9999)           # Generate a plate number
        owner = ForeignKey(Person, 'identifier')    # Reference to an existing person

    generator = DatasetGenerator((Car, 15), (Person, 10))

This way you will generate a dataset containing 15 cars and 10 people, with each car associated to a person. You can visualize it by printing it::

    >> print(generator)
    {'Car': [{'brand': 'Peugeot', 'model': '3008', 'plate': 8321, 'owner': 7}, {'brand': 'Volvo', 'model': 'V60', 'plate': 2509, 'owner': 6}, {'brand': 'Lexus', 'model': 'LX', 'plate': 9135, 'owner': 4}, {'brand': 'Ferrari', 'model': 'DINO', 'plate': 8054, 'owner': 7}, {'brand': 'Renault', 'model': 'LAGUNA', 'plate': 8199, 'owner': 1}, {'brand': 'Audi', 'model': 'A8', 'plate': 8439, 'owner': 9}, {'brand': 'Lexus', 'model': 'ES', 'plate': 1363, 'owner': 10}, {'brand': 'Ferrari', 'model': 'DINO', 'plate': 1670, 'owner': 3}, {'brand': 'Ferrari', 'model': '208', 'plate': 1157, 'owner': 1}, {'brand': 'Ford', 'model': 'FIESTA', 'plate': 9069, 'owner': 6}, {'brand': 'Dacia', 'model': 'LOGAN', 'plate': 6268, 'owner': 9}, {'brand': 'Chevrolet', 'model': 'SONIC', 'plate': 8634, 'owner': 10}, {'brand': 'Mazda', 'model': 'MX-5 MIATA', 'plate': 2442, 'owner': 4}, {'brand': 'Volvo', 'model': 'S90', 'plate': 4562, 'owner': 7}, {'brand': 'Kia', 'model': 'SOUL', 'plate': 5322, 'owner': 6}], 'Person': [{'identifier': 1, 'name': 'Julianna', 'birthdate': '26/05/2000', 'age': 19, 'country': 'Saint Barthélemy'}, {'identifier': 2, 'name': 'Lizbeth', 'birthdate': '20/09/1992', 'age': 27, 'country': 'Ethiopia'}, {'identifier': 3, 'name': 'Kaylie', 'birthdate': '06/05/1990', 'age': 29, 'country': 'Korea, Republic of'}, {'identifier': 4, 'name': 'Simon', 'birthdate': '12/03/2000', 'age': 19, 'country': 'Finland'}, {'identifier': 5, 'name': 'Elisheva', 'birthdate': '09/05/1982', 'age': 37, 'country': 'Chad'}, {'identifier': 6, 'name': 'Bethany', 'birthdate': '17/07/1988', 'age': 31, 'country': 'Chad'}, {'identifier': 7, 'name': 'Eddy', 'birthdate': '24/03/1982', 'age': 37, 'country': 'Nauru'}, {'identifier': 8, 'name': 'Selena', 'birthdate': '21/08/1982', 'age': 37, 'country': 'Réunion'}, {'identifier': 9, 'name': 'Joziah', 'birthdate': '11/01/1988', 'age': 32, 'country': 'Turkey'}, {'identifier': 10, 'name': 'Valentino', 'birthdate': '28/12/1989', 'age': 30, 'country': 'Tonga'}]}

And it can be exported to SQL::

    >> print(generator.to_sql())
    CREATE TABLE IF NOT EXISTS Person (
        identifier INTEGER,
        name VARCHAR(15),
        birthdate DATETIME,
        age DATETIME,
        country VARCHAR(50),
        CONSTRAINT pk_Person PRIMARY KEY (identifier)
    );
    CREATE TABLE IF NOT EXISTS Car (
            brand VARCHAR(15),
            model VARCHAR(25),
            plate INTEGER,
            owner_identifier INTEGER,
            CONSTRAINT fk_owner (owner_identifier) REFERENCES Person(identifier)
    );
    INSERT INTO Person (identifier, name, birthdate, age, country) VALUES (1, "Catherine", "09/10/1981", 38, "Antigua and Barbuda");
    INSERT INTO Person (identifier, name, birthdate, age, country) VALUES (2, "Juliette", "07/01/1995", 25, "Malaysia");
    INSERT INTO Person (identifier, name, birthdate, age, country) VALUES (3, "Ahron", "25/09/1985", 34, "Syrian Arab Republic");
    INSERT INTO Person (identifier, name, birthdate, age, country) VALUES (4, "Emanuel", "28/10/1981", 38, "Uganda");
    INSERT INTO Person (identifier, name, birthdate, age, country) VALUES (5, "Leandro", "04/10/1993", 26, "Burkina Faso");
    INSERT INTO Person (identifier, name, birthdate, age, country) VALUES (6, "Amanda", "28/05/1999", 20, "Uzbekistan");
    INSERT INTO Person (identifier, name, birthdate, age, country) VALUES (7, "Ishmael", "19/01/1995", 24, "Samoa");
    INSERT INTO Person (identifier, name, birthdate, age, country) VALUES (8, "Cormac", "07/02/1986", 33, "Guatemala");
    INSERT INTO Person (identifier, name, birthdate, age, country) VALUES (9, "Stephen", "15/04/1988", 31, "Senegal");
    INSERT INTO Person (identifier, name, birthdate, age, country) VALUES (10, "Lara", "25/07/1984", 35, "Puerto Rico");
    INSERT INTO Car (brand, model, plate, owner_identifier) VALUES ("Volvo", "S90", 9950, 2);
    INSERT INTO Car (brand, model, plate, owner_identifier) VALUES ("Ferrari", "208", 1225, 7);
    INSERT INTO Car (brand, model, plate, owner_identifier) VALUES ("BMW", "F15 X5", 3505, 1);
    INSERT INTO Car (brand, model, plate, owner_identifier) VALUES ("Fiat", "500L", 8031, 10);
    INSERT INTO Car (brand, model, plate, owner_identifier) VALUES ("Fiat", "500L", 2153, 10);
    INSERT INTO Car (brand, model, plate, owner_identifier) VALUES ("Audi", "Q2", 4191, 7);
    INSERT INTO Car (brand, model, plate, owner_identifier) VALUES ("BMW", "F10 5 SERIES", 4197, 9);
    INSERT INTO Car (brand, model, plate, owner_identifier) VALUES ("Volvo", "S60", 9587, 8);
    INSERT INTO Car (brand, model, plate, owner_identifier) VALUES ("Mercedes-Benz", "A-CLASS", 5285, 4);
    INSERT INTO Car (brand, model, plate, owner_identifier) VALUES ("Toyota", "CAMRY", 7922, 3);
    INSERT INTO Car (brand, model, plate, owner_identifier) VALUES ("Kia", "FORTE", 4746, 3);
    INSERT INTO Car (brand, model, plate, owner_identifier) VALUES ("Suzuki", "APV", 7193, 9);
    INSERT INTO Car (brand, model, plate, owner_identifier) VALUES ("BMW", "G06 X6", 6532, 10);
    INSERT INTO Car (brand, model, plate, owner_identifier) VALUES ("Tesla", "MODEL X", 6701, 3);
    INSERT INTO Car (brand, model, plate, owner_identifier) VALUES ("SEAT", "TARRACO", 5301, 6);

.. note::
    To be properly defined and fully compliant with the relational model, Car should have a primary key, which could be the plate number

Please see the full documentation for :class:`dammy.db.DatasetGenerator`.

Extending built-in generators
=============================

If the built-in generators are not enugh for you and the one you need is not available, you can roll your own.
This is a more advanced topic so you should read the :ref:`documentation` and then head to the :ref:`api-reference`.