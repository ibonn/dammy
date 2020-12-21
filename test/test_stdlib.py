import pytest

# Libraries used to perform the tests
import random

# Import everything we need to test
import dammy
from dammy.db import *
from dammy.stdlib import *

def test_bloodtype():
    assert BloodType().generate() == '0+'

def test_carbrand():
    assert CarBrand().generate() == 'BMW'

def test_carmodel():
    assert CarModel().generate() == 'E-Class'

def test_countryname():
    assert CountryName().generate() == 'Grenada'

def test_creditcard():
    assert CreditCard().generate() == '0978 4713 8106 3823'

def test_ipv4address():
    assert IPV4Address().generate() == '139.123.251.45'

@pytest.mark.skip
# TODO mktime overflows in Windows on negative timestamps. Run in other os and set the value here
def test_randomdatetime():
    assert RandomDateTime(date_format='d-m-Y').generate() == ''

def test_randomfloat():
    assert RandomFloat(0, 10).generate() == 1.5376167738406188

def test_randominteger():
    assert RandomInteger(0, 10).generate() == 8

def test_randomname():
    assert RandomName().generate() == 'Reizy'

def test_randomstring():
    assert RandomString(16).generate() == 'DcaiDmbqZwRr9BOA'