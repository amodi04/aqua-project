# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
import math
import numpy as np
from skimage import io
from skimage import img_as_ubyte


def find_red_pixels(*args, **kwargs):
    """
    Finds all the red pixels in the image and produces an output image of the red pixels.
    Parameters:
        map_filename (str): The name of the image located in the data directory.
        upper_threshold (int): The value of the upper threshold for the red value.
        lower_threshold (int): The value of the lower threshold for the green and blue values.
    Returns:
        A 2D numpy matrix of 1's and 0's where 1 represents a red pixel and 0 represents all others.
    """

    map_filename = args[0]
    upper_threshold = kwargs["upper_threshold"]
    lower_threshold = kwargs["lower_threshold"]
    img = io.imread(f"data/{map_filename}")  # Reads the file into a numpy matrix with 3 dimensions

    rows = img.shape[0]
    cols = img.shape[1]
    result = np.zeros((rows, cols))  # Initialises a matrix of 0's with the same resolution as the image

    for i in range(rows):
        for j in range(cols):
            r, g, b, a = img[i][j]  # Unpacks the pixel into RGBA values. The alpha channel is discarded as JPEG does
            # not support transparency
            if r > upper_threshold and g < lower_threshold and b < lower_threshold:
                result[i][j] = 1  # Requirements met for red pixel
    io.imsave("map-red-pixels.jpg", result)  # Save matrix into a JPEG image
    return result


def find_cyan_pixels(*args, **kwargs):
    """
    Finds all the cyan pixels in the image and produces an output image of the red pixels.
    Parameters:
        map_filename (str): The name of the image located in the data directory.
        upper_threshold (int): The value of the upper threshold for the green and blue values.
        lower_threshold (int): The value of the lower threshold for the red value.
    Returns:
        A 2D numpy matrix of 1's and 0's where 1 represents a cyan pixel and 0 represents all others.
    """

    map_filename = args[0]
    upper_threshold = kwargs["upper_threshold"]
    lower_threshold = kwargs["lower_threshold"]
    img = io.imread(f"data/{map_filename}")  # Reads the file into a numpy matrix with 3 dimensions
    rows = img.shape[0]
    cols = img.shape[1]
    result = np.zeros((rows, cols))  # Initialises a matrix of 0's with the same resolution as the image

    for i in range(rows):
        for j in range(cols):
            r, g, b, a = img[i][j]  # Unpacks the pixel into RGBA values. The alpha channel is discarded as JPEG does
            # not support transparency
            if r < lower_threshold and g > upper_threshold and b > upper_threshold:
                result[i][j] = 1  # Requirements met for cyan pixel
    io.imsave("map-cyan-pixels.jpg", result)  # Save matrix into a JPEG image
    return result


def detect_connected_components(*args, **kwargs):
    """
    Finds all the connected components in the matrix passed in. Also writes number of pixels per components to a text file.
    Algorithm improvements: The algorithm has been modified to count the number of pixels per connected component by
    assigning a unique number to each pixel depending on which connected component they are in. The output of mark is
    therefore the same as img except that the 1's are now changed into a variety of integer values showing the
    connected component that hte pixel belongs to. The algorithm can be further improved by removing the gathering
    of all 8-neighbours if they those neighbours have already been checked on a previous pass.
    Parameters:
        img (numpy.ndarray): The matrix of 1's and 0's in which to find the connected components.
    Returns:
        A 2D numpy array consisting of the different connected components identified by a unique ID.
    """
    # TODO: add unit tests to utils
    img = args[0]
    mark = np.zeros(img.shape)  # Create matrix of same size as the matrix passed in
    q = np.empty((0, 2), int)  # Creates an empty ndarray with shape (0,2) and holds integers
    count = 0
    connected_components = 0
    with open("cc-output-2a.txt", "w") as f:  # Creates the empty text file
        pass
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            pixel = img[x][y]
            if pixel == 1 and mark[x][y] == 0:  # If pixel is part of a component but not visited
                print(pixel)
                mark[x][y] = connected_components + 1  # Set as visited
                count += 1  # Increase number of pixels in this connected component
                q = np.append(q, np.array([[x, y]]), axis=0)  # Add this pixel to the queue of pixels to visit
                while len(q) > 0:
                    item = q[0]
                    q = np.delete(q, 0, axis=0)  # Remove pixel visited from the queue
                    neighbours = get_neighbours(item, img.shape)  # Get all neighbours of pixel
                    print(neighbours)
                    exit()
                    for nx, ny in neighbours:
                        if img[nx][ny] == 1 and mark[nx][ny] == 0:  # If neighbour is part of a component but not
                            # visited
                            mark[nx][ny] = connected_components + 1  # Set as visited
                            count += 1  # Increase number of pixels in this connected component
                            q = np.append(q, np.array([[nx, ny]]), axis=0)  # Add this neighbour to the queue of
                            # pixels to visit
                connected_components += 1  # Move to next connected component when no more pixels left in this one
                with open("cc-output-2a.txt", "a") as f:
                    f.write(f"Connected Component {connected_components}, number of pixels = {count}\n")
                count = 0
    with open("cc-output-2a.txt", "a") as f:
        f.write(f"Total number of connected components = {connected_components}")
    return mark


def get_neighbours(pixel, map_size):
    """
    Finds all the neigbours of the given pixel.
    Parameters:
        pixel (tuple): The coordinates of the pixel to check.
        map_size (tuple): The resolution of the map to check edge conditions.
    Returns:
        A list of the coordinates of the neighbours of the pixel.
    """
    x, y = pixel
    x_bound, y_bound = map_size
    neighbours = [(x2, y2) for x2 in range(x - 1, x + 2) for y2 in range(y - 1, y + 2)
                  if (-1 < x < x_bound and -1 < y < y_bound and (x != x2 or y != y2) and
                      (0 <= x2 < x_bound) and (0 <= y2 < y_bound))]  # Adds all neighbours and checks edge conditions
    return neighbours


def detect_connected_components_sorted(*args, **kwargs):
    """
    Finds all the connected components and sorts them in descending order. Also writes the two largest components to an image.
    Parameters:
        mark (numpy.ndarray): The matrix of connected components.
    """

    mark = args[0]
    with open("cc-output-2b.txt", "w") as f:  # Creates the empty text file
        pass
    components, pixels = np.unique(mark, return_counts=True)  # Counts the number of each pixel per component from
    # the passed in matrix
    components = components[1:]  # Removes component 0 as that is the black component of the image
    pixels = pixels[1:]  # Removes the number of pixels in the black component
    array = list(zip(components, pixels))
    quick_sort(array, 0, len(components) - 1)  # Sort into descending order
    for i, j in array:
        with open("cc-output-2b.txt", "a") as f:
            f.write(f"Connected Component {int(i)}, number of pixels = {j}\n")
    with open("cc-output-2b.txt", "a") as f:
        f.write(f"Total number of connected components = {len(components)}")
    write_top_two(mark, [i for i, j in array[:2]])


def write_top_two(mark, top_two):
    """
    Writes the two largest connected components into an image.
    Parameters:
        mark (numpy.ndarray): The matrix of connected components.
        top_two (list): The ID's for the top two connected components.
    """

    mark[(mark != top_two[0]) & (mark != top_two[1])] = 0  # Set all pixels to 0 if they are not part of the top two
    mark[mark != 0] = 1  # Set all remaining pixels to 1 (the top two connected components)
    io.imsave("cc-top-2.jpg", img_as_ubyte(mark))


def quick_sort(array, low, high):
    """
    Sorts an array of numbers in descending order via the quick sort algorithm.
    Parameters:
         array (list): The list to sort.
         low: (int): The index of the start of the sublist.
         high (int): The index of the end of the sublist.
    """

    if 0 <= low < high:
        pivot = partition(array, low, high)  # Calculate pivot at which to split the array into sub arrays
        quick_sort(array, low, pivot)  # Sort left sublist
        quick_sort(array, pivot + 1, high)  # Sort right sublist


def partition(array, low, high):
    """
    Partitions and sorts the sub-array. Uses the Hoare partition scheme for better efficiency.
    Parameters:
        array (list): The array to sort.
        low (int): The index of the start of the sub-array.
        high (int): The index of the end of the sub-array.
    Returns:
        An integer partition index.
    """

    pivot = array[math.floor((high + low) / 2)][1]  # Get value at middle of sub-array
    left = low - 1
    right = high + 1
    while True:
        while True:
            left += 1
            if array[left][1] <= pivot:
                break
        while True:
            right -= 1
            if array[right][1] >= pivot:
                break
        if left >= right:
            return right  # Return index at which pointers cross
        array[left], array[right] = array[right], array[left]  # Swap values
