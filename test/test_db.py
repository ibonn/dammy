import pytest

# Libraries used to perform the tests
import random

# Import everything we need to test
import dammy
from dammy.db import *
from dammy.stdlib import RandomInteger

def test_empty_key_exeption():
    with pytest.raises(dammy.exceptions.EmptyKeyException):
        class A(dammy.EntityGenerator):
            key = PrimaryKey()

def test_dataset_required_exception():

    class A(dammy.EntityGenerator):
        key = PrimaryKey(id=AutoIncrement())

    class B(dammy.EntityGenerator):
            ref_to_A = ForeignKey(A, 'key')

    with pytest.raises(dammy.exceptions.DatasetRequiredException):
        B().generate()
    
def test_unique():
    x = Unique(id=RandomInteger(1, 10))

    with pytest.raises(dammy.exceptions.MaximumRetriesExceededException):
        for _ in range(0, 50):
            print(x)            # Exception after generating 10 values