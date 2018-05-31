import pytest
from itertools import islice

def test_allthesame_tuples():
    #   We use tuples here rather than lists because we want to ensure that
    #   this `allthesame` predicate, which is supposed to be just telling us
    #   something about our data structure, is not also modifying it as well.

    for xs in [ (), (3,), (3,3), (3,3,3), (3,3,3,3,3,3) ]:
        assert allthesame(xs) is True
    for ys in [ (3,4), (3,4,3), (3,3,3,3,3,4) ]:
        assert allthesame(ys) is False

def test_allthesame_strs():
    assert allthesame('')     is True
    assert allthesame('wwww') is True
    assert allthesame('bad')  is False

def test_allthesame_infinite():
    def intgenerator():
        '   Return a hundred or so 0s, then a hundred or so 1s, ...   '
        #   We could be more clever here but that's not what this
        #   tutorial is about.
        n = 0
        while True:
            yield int(n)
            n += 0.01

    #   And a little test of the generator for anybody who's nervous.
    #   It's infinite, but we can look at just a few specific values.
    assert [0, 0, 1, 1, 2, 2, 2, 3, 3, 4] \
        == list(islice(intgenerator(), 0, 500, 50))

    assert not allthesame(intgenerator())

@pytest.mark.skip('This test takes too long to run.')
def test_allthesame_nonterminate():
    assert allthesame(repeat(17))


def allthesame(iterable):
    iterator = iterable.__iter__()
    try:
        x0 = next(iterator)
        for x in iterator:
            if x != x0: return False
        return True
    except StopIteration:
        return True
