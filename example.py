from core import DammyEntity
from stdlib import RandomInteger, RandomName, CarBrand, CarModel, RandomString

# Define what a person looks like
class Person(DammyEntity):
    name = RandomName(language_code='es')
    age = RandomInteger(0, 100)
    password = RandomString(32)

class Car(DammyEntity):
    brand = CarBrand()
    model = CarModel(car_brand=brand)
    owner = Person()

# Generate 100 random people
for i in range(0, 100):
    print(Car())