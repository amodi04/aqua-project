# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification


def sumvalues(values):
    """
    Sums a list of numerical values.
    Parameters:
        values (list): The array of values to sum.
    Returns:
        The sum value.
    """

    total = 0
    for i in values:
        try:
            total += float(i)  # Only allow numerical values
        except ValueError as ex:
            print(ex.args)
    return total


def maxvalue(values):
    """
    Calculates the index of the max value in an array.
    Parameters:
        values (list): The array to search.
    Returns:
        The index of the maximum value.
    """

    index_highest = 0
    for i, j in enumerate(values):
        try:
            n = float(j)  # Only allow numerical values
            if n > values[index_highest]:
                index_highest = i
        except ValueError as ex:
            print(ex.args)
    return index_highest


def minvalue(values):
    """
    Calculates the index of the minimum value in an array.
    Parameters:
        values (list): The array to search.
    Returns:
        The index of the minimum value.
    """

    index_lowest = 0
    for i, j in enumerate(values):
        try:
            n = float(j)  # Only allow numerical values
            if n < values[index_lowest]:
                index_lowest = i
        except ValueError as ex:
            print(ex.args)
    return index_lowest


def meannvalue(values):
    """
    Calculates the average / mean value of an array.
    Parameters:
        values (list): The list to calculate the arithmetic mean from.
    Returns:
        The mean value.
    """

    total = 0
    for i in values:
        try:
            total += float(i)  # Only allow numerical values
        except ValueError as ex:
            print(ex.args)
    return total / len(values)


def countvalue(values, x):
    """
    Counts the number of times x appears in the list of values.
    Parameters:
        values (list): The list of values to search.
        x (float/int): The number to count occurrences of.
    Returns:
        The number of occurrences.
    """

    count = 0
    for i in values:
        if i == x:
            count += 1
    return count


def split(array, n):
    """
    Splits an array into specified chunks of size n.
    Parameters:
        array (list): The list of values to split.
        n (int): The size of each chunk.
    Returns:
        A generator object containing the sub-lists of size n.
    """

    for i in range(0, len(array), n):
        yield array[i:i + n]


def insertion_sort(array):
    """
    Uses the insertion sort algorithm to sort an array of numerical values into ascending order.
    Parameters:
        array (list): The array to sort.
    Returns:
        An array sorted in ascending order.
    """

    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and key < array[j]:  # Move elements greater than key to one position ahead of current position
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
    return array


def format_message(message, *args):
    """
    Formats a string with colors.
    Parameters:
        message (str): The string to format
        args (color): The colors to apply to the string.
    Returns:
        The message formatted with colors.
    """

    formatted = ""
    for i in args:  # Apply colors at start of string
        formatted += i
    formatted += message + color.END  # End formatting
    return formatted


class color:
    """
    Class of available formatting options for strings for console output.
    """
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
