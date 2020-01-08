from datetime import datetime
from core import DammyEntity, DatasetGenerator
from stdlib import RandomInteger, RandomName, CarBrand, CarModel, RandomString, RandomDateTime, AutoIncrement

# Define what a person looks like
class Person(DammyEntity):
    identifier = AutoIncrement()
    name = RandomName(language_code='es')
    password = RandomString(5)
    birthday = RandomDateTime(start=datetime(1980, 1, 1), end=datetime(2000, 12, 31), date_format='%d/%m/%Y')
    favorite_number = RandomInteger(0, 10)
    # age = datetime.now() - birthday   # TODO possible idea for the future

class Car(DammyEntity):
    brand = CarBrand()
    model = CarModel(car_brand=brand)
    owner = 'Person__identifier'

# Generate 10 random people
for i in range(0, 10):
    print(Person())

# Generate a dataset with 3 people and 7 cars
dataset = DatasetGenerator((Car, 7), (Person, 3))
print(dataset)