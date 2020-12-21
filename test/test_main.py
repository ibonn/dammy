import pytest

# Libraries used to perform the tests
import random

# Import everything we need to test
import dammy
from dammy.stdlib import RandomInteger
from dammy.functions import *

# Test the seed function
def test_seed():
    """
    When the seed is set to 123 the random integer between 0 and 100000 must be 6863
    """
    dammy.seed(123)
    assert random.randint(0, 100000) == 6863

# Test API
def test_generate_raw_not_implemented():
    """
    A NotImplementedError is raised if the generate_raw() method is not implemented
    """
    class DummyGenerator(dammy.BaseGenerator):
        
        def __init__(self):
            super(DummyGenerator, self).__init__('VARCHAR(10)')

    with pytest.raises(NotImplementedError):
        DummyGenerator().generate_raw()

# Test operators
def test_operators():
    """
    Tests operations between generators
    """
    class DummyEntity(dammy.EntityGenerator):
        a = RandomInteger(0, 100)
        b = RandomInteger(0, 100)
        
        sub = a - b
        add = a + b
        div = a / b
        mul = a * b

        eq = a == b
        lt = a < b
        gt = a > b
        le = a <= b
        ge = a >= b

    g = DummyEntity().generate()

    assert g['a'] == 34
    assert g['b'] == 11

    assert g['sub'] == 23           # 34 - 11 = 23
    assert g['add'] == 45           # 34 + 11 = 45
    assert g['div'] == 34 / 11      # 34 / 11 = 3.090909...
    assert g['mul'] == 374          # 34 * 11 = 374

    assert not g['eq']              # 34 == 11 -> FALSE
    assert not g['lt']              # 34 < 11 -> FALSE
    assert g['gt']                  # 34 > 11 -> TRUE
    assert not g['le']              # 34 <= 11 -> FALSE
    assert g['ge']                  # 34 >= 11 -> TRUE

@pytest.mark.xfail
# BUG call_function() generates a new random integer instead of using the one in a
def test_functions():
    """
    Tests funtion calls
    """
    class DummyEntity(dammy.EntityGenerator):
        a = RandomInteger(0, 100)
        b = call_function(a, lambda x : x + 3)

    g = DummyEntity().generate()

    assert g['a'] == 98
    assert g['b'] == 101