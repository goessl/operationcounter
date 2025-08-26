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
