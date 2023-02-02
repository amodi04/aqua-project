import utils


def test_sumvalues():
    """
    Tests the sum of integers of the list of natural numbers up to 10.
    """

    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert utils.sumvalues(values) == 55


def test_maxvalue():
    """
    Tests the index of the maximum value of the list of natural numbers up to 10.
    """

    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert utils.maxvalue(values) == 9


def test_minvalue():
    """
    Tests the index of the minimum value of the list of natural numbers up to 10.
    """

    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert utils.minvalue(values) == 0


def test_meanvalue():
    """
    Tests the mean value of the list of natural numbers up to 10.
    """

    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert utils.meannvalue(values) == 5.5


def test_countvalue():
    """
    Tests the number of occurrences of the value 1 in the list.
    """

    values = [1, 1, 1, 2, 2, 3, 3, 4, 5, 6, 7, 7, 8, 9, 10]
    assert utils.countvalue(values, 1) == 3


def test_split():
    """
    Tests if the list is split correctly.
    """

    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert len(list(utils.split(values, 5))) == 2


def test_insertion_sort():
    """
    Tests if the insertion sort function works correctly by sorting in ascending order.
    """

    values = [1, 6, 3, 8, 2, 9, 10, 7, 0]
    assert utils.insertion_sort(values) == [0, 1, 2, 3, 6, 7, 8, 9, 10]



