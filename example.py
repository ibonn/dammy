from datetime import datetime
from core import DammyEntity, DatasetGenerator
from stdlib import RandomInteger, RandomName, CarBrand, CarModel, RandomString, RandomDateTime
from db import AutoIncrement

# Define what a person looks like
class Person(DammyEntity):
    identifier = AutoIncrement()
    name = RandomName(language_code='es')
    password = RandomString(5)
    birthday = RandomDateTime(start=datetime(1980, 1, 1), end=datetime(2000, 12, 31), date_format='%d/%m/%Y')
    favorite_number = RandomInteger(0, 10)
    # age = datetime.now() - birthday   # TODO possible idea for the future

# Define what a car looks like
class CarManufacturer(DammyEntity):
    identifier = AutoIncrement()
    manufacturer_name = CarBrand()

class Car(DammyEntity):
    brand = 'CarManufacturer__manufacturer_name'
    model = CarModel(car_brand=brand)
    owner = 'Person__identifier'

# Generate 10 random people
# for i in range(0, 10):
#     print(Person())

# Generate a dataset with 3 people and 7 cars
dataset = DatasetGenerator((Car, 7), (CarManufacturer, 2), (Person, 3))
print(dataset.get_sql())