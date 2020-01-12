from datetime import datetime
from core import DammyEntity, DatasetGenerator
from stdlib import RandomInteger, RandomName, CarBrand, CarModel, RandomString, RandomDateTime, CountryName
from db import AutoIncrement, ForeignKey, PrimaryKey

# Define what a person looks like
class Person(DammyEntity):
    identifier = AutoIncrement()
    first_name = PrimaryKey(RandomName(language_code='es'))
    last_name = PrimaryKey(RandomName(language_code='es'))
    password = RandomString(5)
    birthday = RandomDateTime(start=datetime(1980, 1, 1), end=datetime(2000, 12, 31), date_format='%d/%m/%Y')
    favorite_number = RandomInteger(0, 10)
    age = datetime.now() - birthday
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
    owner = ForeignKey(Person, 'first_name', 'last_name')

# Generate 10 random people
# for i in range(0, 10):
#     print(Person())

# Generate a dataset with 94234 people, 8 manufacturers and 20000 cars
dataset = DatasetGenerator((Car, 3), (CarManufacturer, 8), (Person, 4))

# print(dataset)
print(dataset.get_sql(save_to='dataset.sql'))      # Save to sql (Beta)