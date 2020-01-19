import random
from datetime import datetime

from dammy import EntityGenerator
from dammy.functions import cast
from dammy.stdlib import RandomInteger, RandomName, CarBrand, CarModel, RandomString, RandomDateTime, CountryName, BloodType
from dammy.db import AutoIncrement, ForeignKey, PrimaryKey, Unique, DatasetGenerator

# Set the seed to make the results replicable
random.seed(1234)

# Define what a person looks like
class Person(EntityGenerator):
    id_pk = PrimaryKey(identifier=AutoIncrement())
    uid_uq = Unique(uid=RandomString(5))
    first_name = RandomName().upper()
    blood = BloodType()
    birthday = RandomDateTime(start=datetime(1980, 1, 1), end=datetime(2000, 12, 31), date_format='%d/%m/%Y')
    favorite_number = RandomInteger(0, 10)
    age = cast((datetime.now() - birthday).days / 365.25, int)
    country = CountryName()

# Define what a car manufacturer looks like
class CarManufacturer(EntityGenerator):
    id_pk = PrimaryKey(identifier=AutoIncrement())
    manufacturer_uq = Unique(manufacturer_name=CarBrand())
    constant_field = True

# Define what a car looks like
class Car(EntityGenerator):
    car_pk = PrimaryKey(car_id=AutoIncrement())
    brand = ForeignKey(CarManufacturer, 'manufacturer_uq')
    model = CarModel(car_brand=brand)
    owner = ForeignKey(Person, 'id_pk')

# Generate 10 random people
for i in range(0, 10):
    print(Person())

# Save 54 instances of people to json and 12 to csv
Person().to_json(54, 'people.json')
Person().to_csv(12, 'people.csv')

# Generate a dataset with 1500 people, 8 manufacturers and 1000 cars
dataset = DatasetGenerator((Car, 1000), (CarManufacturer, 8), (Person, 1500)).generate()

# print(dataset)                        # Prints the dataset as a dict (Not recommended, dataset is quite large)
dataset.get_sql(save_to='dataset.sql')  # Save to sql
dataset.to_json('dataset.json')         # Save to json (Beta)