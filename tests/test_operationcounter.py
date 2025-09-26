from operationcounter import *
import numpy as np

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

def test_wrapping():
    #sequence
    t = (1, 2, 3)
    assert OperationCounter.wrapCollection(t) == \
            (OperationCounter(1), OperationCounter(2), OperationCounter(3))
    
    t = OperationCounter.wrapCollection(t)
    assert OperationCounter.unwrapCollection(t) == (1, 2, 3)
    
    #mapping
    d = {1:2, 3:4}
    assert OperationCounter.wrapCollection(d) == \
            {OperationCounter(1):OperationCounter(2),
             OperationCounter(3):OperationCounter(4)}
    
    d = OperationCounter.wrapCollection(d)
    assert OperationCounter.unwrapCollection(d) == {1:2, 3:4}
    
    #array
    a = np.array([1, 2])
    assert np.array_equal(OperationCounter.wrapArray(a),
            np.array([OperationCounter(1), OperationCounter(2)]))
    
    a = OperationCounter.unwrapArray(a)
    assert np.array_equal(OperationCounter.unwrapArray(a), np.array([1, 2]))
