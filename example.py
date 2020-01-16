import random
from datetime import datetime

from dammy import DammyEntity, DatasetGenerator
from dammy.stdlib import RandomInteger, RandomName, CarBrand, CarModel, RandomString, RandomDateTime, CountryName
from dammy.db import AutoIncrement, ForeignKey, PrimaryKey

# Set the seed to make the results replicable
random.seed(1234)

# Define what a person looks like
class Person(DammyEntity):
    identifier = PrimaryKey(AutoIncrement())
    first_name = RandomName().upper()
    password = RandomString(5)
    birthday = RandomDateTime(start=datetime(1980, 1, 1), end=datetime(2000, 12, 31), date_format='%d/%m/%Y')
    favorite_number = RandomInteger(0, 10)
    age = (datetime.now() - birthday).days / 365.25
    country = CountryName()

# Define what a car looks like
class CarManufacturer(DammyEntity):
    identifier = AutoIncrement()
    manufacturer_name = PrimaryKey(CarBrand())
    constant_field = True

class Car(DammyEntity):
    car_id = PrimaryKey(AutoIncrement())
    brand = ForeignKey(CarManufacturer, 'manufacturer_name')
    model = CarModel(car_brand=brand)
    owner = ForeignKey(Person, 'identifier')

# Generate 10 random people
for i in range(0, 10):
    print(Person())

# Generate a dataset with 94234 people, 8 manufacturers and 20000 cars
dataset = DatasetGenerator((Car, 10), (CarManufacturer, 5), (Person, 7))

print(dataset)                          # Prints the dataset as a dict
dataset.get_sql(save_to='dataset.sql')  # Save to sql (Beta)