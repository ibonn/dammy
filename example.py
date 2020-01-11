from datetime import datetime
from core import DammyEntity, DatasetGenerator
from stdlib import RandomInteger, RandomName, CarBrand, CarModel, RandomString, RandomDateTime, CountryName
from db import AutoIncrement, ForeignKey

# Define what a person looks like
class Person(DammyEntity):
    identifier = AutoIncrement()
    first_name = RandomName(language_code='es')
    last_name = RandomName(language_code='es')
    password = RandomString(5)
    birthday = RandomDateTime(start=datetime(1980, 1, 1), end=datetime(2000, 12, 31), date_format='%d/%m/%Y')
    favorite_number = RandomInteger(0, 10)
    age = datetime.now() - birthday
    country = CountryName()

# Define what a car looks like
class CarManufacturer(DammyEntity):
    identifier = AutoIncrement()
    manufacturer_name = CarBrand()
    constant_field = True

class Car(DammyEntity):
    brand = ForeignKey(CarManufacturer, 'manufacturer_name')
    model = CarModel(car_brand=brand)
    owner = ForeignKey(Person, 'identifier')

# Generate 10 random people
# for i in range(0, 10):
#     print(Person())

# Generate a dataset with 94234 people, 8 manufacturers and 20000 cars
dataset = DatasetGenerator((Car, 20000), (CarManufacturer, 8), (Person, 94234))

dataset.get_sql(save_to='dataset.sql')      # Save to sql (Beta)