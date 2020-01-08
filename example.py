from datetime import datetime
from core import DammyEntity
from stdlib import RandomInteger, RandomName, CarBrand, CarModel, RandomString, RandomDateTime, AutoIncrement

# Define what a person looks like
class Person(DammyEntity):
    identifier = AutoIncrement()
    name = RandomName(language_code='es')
    age = RandomInteger(0, 100)
    password = RandomString(32)
    birthday = RandomDateTime(start=datetime(1980, 1, 1), end=datetime(2000, 12, 31), date_format='%d/%m/%Y')

class Car(DammyEntity):
    brand = CarBrand()
    model = CarModel(car_brand=brand)
    owner = Person()

# Generate 100 random cars
for i in range(0, 99):
    print(Car())