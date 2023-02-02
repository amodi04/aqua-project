import os.path
import intelligence


def test_find_red_pixels():
    """
    Tests that the output file is created.
    """

    intelligence.find_red_pixels("map.png", upper_threshold=100, lower_threshold=50)
    assert os.path.exists("map-red-pixels.jpg")


def test_find_cyan_pixels():
    """
    Tests that the output file is created.
    """

    intelligence.find_cyan_pixels("map.png", upper_threshold=100, lower_threshold=50)
    assert os.path.exists("map-cyan-pixels.jpg")


def test_detect_connected_components():
    """
    Tests that the returned 2D array has the same dimensions as the image passed in.
    """

    result = intelligence.find_red_pixels("map.png", upper_threshold=100, lower_threshold=50)
    mark = intelligence.detect_connected_components(result)
    assert mark.shape == (1140, 1053)


def test_get_neighbours():
    """
    Tests that the correct neighbours are calculated.
    """

    assert intelligence.get_neighbours((0, 0), (100, 100)) == [(0, 1), (1, 0), (1, 1)]


def test_detect_connected_components_sorted():
    """
    Tests that the output file is created.
    """

    result = intelligence.find_red_pixels("map.png", upper_threshold=100, lower_threshold=50)
    mark = intelligence.detect_connected_components(result)
    intelligence.detect_connected_components_sorted(mark)
    assert os.path.exists("cc-output-2b.txt")


def test_write_top_two():
    """
    Tests that the output file is created.
    """

    result = intelligence.find_red_pixels("map.png", upper_threshold=100, lower_threshold=50)
    mark = intelligence.detect_connected_components(result)
    intelligence.detect_connected_components_sorted(mark)
    assert os.path.exists("cc-top-2.jpg")


def test_quick_sort():
    """
    Tests that the quick sort function correctly sorts the numbers in descending order.
    """

    num = [22, 67, 61, 93, 31, 12, 33, 70, 78, 12, 40, 78, 66, 12, 32, 7, 37, 11, 48, 65, 69, 20, 23, 31]
    print(num)
    letters = "abcdefghij"
    array = list(zip(letters, num))
    intelligence.quick_sort(array, 0, len(array) - 1)
    assert array == [('d', 93), ('i', 78), ('h', 70), ('b', 67), ('c', 61), ('g', 33), ('e', 31), ('a', 22), ('j', 12), ('f', 12)]
