from operationcounter import *

def test_sum_default():
    a = (1, 2, 3, 4)
    a = tuple(map(OperationCounter, a))
    
    with count_ops() as counts:
        assert sum_default(a) == 10
        assert counts == {'add':3, 'eq':1}
    assert sum_default(()) == 0
    assert sum_default((), 2) == 2

def test_prod_default():
    a = (1, 2, 3, 4)
    a = tuple(map(OperationCounter, a))
    
    with count_ops() as counts:
        assert prod_default(a) == 24
        assert counts == {'mul':3, 'eq':1}
    assert prod_default(()) == 1
    assert prod_default((), 2) == 2

def test_sumprod_default():
    a = (1, 2, 3, 4)
    b = (5, 6, 7, 8, 9)
    a, b = tuple(map(OperationCounter, a)), tuple(map(OperationCounter, b))
    
    with count_ops() as counts:
        assert sumprod_default(a, b) == 70
        assert counts == {'mul':4, 'add':3, 'eq':1}
    assert sumprod_default((), ()) == 0
    assert sumprod_default((), (), 2) == 2
