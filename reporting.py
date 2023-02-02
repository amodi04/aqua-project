# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
from itertools import accumulate
import pandas as pd
from collections import Counter
from utils import split, insertion_sort


def daily_average(data, monitoring_station, pollutant):
    """
    Calculates the average value each day for a particular pollutant and monitoring station.
    Parameters:
        data (dict): Dictionary containing pandas DataFrames for each monitoring station.
        monitoring_station (str): The name of the monitoring station.
        pollutant (str): The name of the pollutant.
    Returns:
        A list of 365 numerical values representing the average for each day of the year.
    """

    station_data = data[monitoring_station]
    pollutant_values = station_data[pollutant]
    result = []

    daily_entries = list(split(pollutant_values, 24))  # Split values into chunks of 24 hour periods
    for day in daily_entries:
        day_total = 0
        filtered_day = list(filter(lambda x: x != "No data", day))  # Ignore any "No data" values
        if len(filtered_day) == 0:
            result.append("No data for this day")
            continue
        for value in filtered_day:
            day_total += float(value)
        result.append(day_total / len(filtered_day))
    return result


def daily_median(data, monitoring_station, pollutant):
    """
    Calculates the median value each day for a particular pollutant and monitoring station.
    Parameters:
        data (dict): Dictionary containing pandas DataFrames for each monitoring station.
        monitoring_station (str): The name of the monitoring station.
        pollutant (str): The name of the pollutant.
    Returns:
        A list of 365 numerical values representing the median for each day of the year.
    """

    station_data = data[monitoring_station]
    pollutant_values = station_data[pollutant]
    result = []

    daily_entries = list(split(pollutant_values, 24))  # Split values into chunks of 24 hour periods
    for day in daily_entries:
        filtered_day = list(filter(lambda x: x != "No data", day))  # Ignore any "No data" values
        if len(filtered_day) == 0:
            result.append("No data for this day")
            continue
        sorted_day = insertion_sort([float(i) for i in filtered_day])  # Sort data into ascending order
        mid = len(sorted_day) // 2
        median = (sorted_day[mid] + sorted_day[~mid]) / 2  # Calculate average of middle values
        result.append(median)
    return result


def hourly_average(data, monitoring_station, pollutant):
    """
    Calculates the average for each hour across all 365 days
    of the year for a particular pollutant and monitoring station.
    Parameters:
        data (dict): Dictionary containing pandas DataFrames for each monitoring station.
        monitoring_station (str): The name of the monitoring station.
        pollutant (str): The name of the pollutant.
    Returns:
        A list of 24 numerical values representing the average for each hour of a day.
    """

    station_data = data[monitoring_station]
    pollutant_values = station_data[pollutant].values
    result = []

    hourly_entries = [pollutant_values[i::24] for i in range(24)]  # Stores values for the same hour in a sublist
    for hour in hourly_entries:
        hour_total = 0
        filtered_hour = list(filter(lambda x: x != "No data", hour))  # Ignore any "No data" values
        for value in filtered_hour:
            hour_total += float(value)
        result.append(hour_total / len(filtered_hour))
    return result


def monthly_average(data, monitoring_station, pollutant):
    """
    Calculates the average for each month of the year for a particular pollutant and monitoring station.
    Parameters:
        data (dict): Dictionary containing pandas DataFrames for each monitoring station.
        monitoring_station (str): The name of the monitoring station.
        pollutant (str): The name of the pollutant.
    Returns:
        A list of 12 numerical values representing the average for each month of the year.
    """

    station_data = data[monitoring_station]
    pollutant_values = station_data[pollutant].values
    date_values = station_data["date"]
    result = []

    months = [date[5:7] for date in date_values]  # Stores the month number for each entry in the dataset
    num_entries_in_month = Counter(
        map(lambda x: int(x), months)).values()  # Counts the number of occurrences of each month in the dataset
    monthly_entries = [pollutant_values[x - y:x] for x, y in
                       zip(accumulate(num_entries_in_month),
                           num_entries_in_month)]  # Splits the data based on number of entries each month
    for month in monthly_entries:
        month_total = 0
        filtered_month = list(filter(lambda x: x != "No data", month))  # Ignore any "No data" values
        if len(filtered_month) == 0:
            result.append("No data for this month")
            continue
        for value in filtered_month:
            month_total += float(value)
        result.append(month_total / len(filtered_month))
    return result


def peak_hour_date(data, date, monitoring_station, pollutant):
    """
    Finds the hour and value at a particular monitoring station and date for which the specified pollutant is highest.
    Parameters:
        data (dict): Dictionary containing pandas DataFrames for each monitoring station.
        date (str): The date on which to find the peak value.
        monitoring_station (str): The name of the monitoring station.
        pollutant (str): The name of the pollutant.
    Returns:
        A list of 12 numerical values representing the average for each month of the year.
    """

    station_data = data[monitoring_station]
    pollutant_values = station_data[pollutant]

    date_values = station_data["date"]  # Get date column
    hour_indices = [i for i, x in enumerate(date_values) if
                    x == date]  # Get the indices in the dataset for all hours of the specific date
    highest = ("", 0)
    for i, j in enumerate(hour_indices):
        if pollutant_values[j] == "No data":
            continue
        if float(pollutant_values[j]) > highest[1]:  # If greater than current greatest
            highest = (f"{i + 1}:00", float(pollutant_values[j]))  # Store hour along with value
    return highest


def count_missing_data(data, monitoring_station, pollutant):
    """
    Counts number of occurrences of "No data" for a particular monitoring station and pollutant.
    Parameters:
        data (dict): Dictionary containing pandas DataFrames for each monitoring station.
        monitoring_station (str): The name of the monitoring station.
        pollutant (str): The name of the pollutant.
    Returns:
        An integer representing the number of missing data values.
    """

    station_data = data[monitoring_station]
    pollutant_values = station_data[pollutant]

    return len(list(
        filter(lambda x: x == "No data", pollutant_values)))  # Filters out anything but "No data" and counts length


def fill_missing_data(data, new_value, monitoring_station, pollutant):
    """
    Replaces "No data" values with a specified value for a particular monitoring station and pollutant.
    Parameters:
        data (dict): Dictionary containing pandas DataFrames for each monitoring station.
        new_value: The value to replace the "No data".
        monitoring_station (str): The name of the monitoring station.
        pollutant (str): The name of the pollutant.
    Returns:
        A dictionary object containing no missing data for a particular monitoring station and pollutant.
    """

    station_data = data[monitoring_station]
    pollutant_values = station_data[pollutant]

    new_pollutant_values = list(map(lambda x: new_value if x == "No data" else x,
                                    pollutant_values))  # Maps the new value to the missing data value
    data[monitoring_station][pollutant] = new_pollutant_values  # Replaced old data with new data
    return data


def load_data():
    """
    Loads the csv files into a dictionary of Pandas Dataframes.
    Returns:
        A dictionary containing three dataframes - one for each csv.
    """

    m_data = pd.read_csv("data/Pollution-London Marylebone Road.csv")
    h_data = pd.read_csv("data/Pollution-London Harlington.csv")
    k_data = pd.read_csv("data/Pollution-London N Kensington.csv")

    return {"Marylebone Road": m_data, "Harlington": h_data, "N Kensington": k_data}
