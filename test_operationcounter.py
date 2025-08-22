from operationcounter import *

def test_operationcounter():
    with count_ops() as counts:
        a = OperationCounter(3)
        b = OperationCounter(5)
        c = a * b + 2
        if c > 10:
            c -= 1
        
        assert c.v == 16
        assert counts == {'add':1, 'isub':1, 'mul':1, 'gt':1}
        assert OperationCounter.grouped(counts) \
                == {'add':1, 'sub':1, 'mul':1, 'cmp':1}

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
