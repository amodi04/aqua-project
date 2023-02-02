# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
import os.path
from utils import color, format_message
import intelligence, reporting, monitoring


def main_menu():
    """
    The main entry point for the program.
    """
    print(format_message("Welcome to AQUA!", color.BOLD, color.CYAN))
    show_options()
    while True:  # Ensures user only enters valid options
        user_choice = input(format_message("Enter an option: ", color.BOLD, color.PURPLE)).upper()
        if user_choice == "R":
            reporting_menu()
            break
        elif user_choice == "I":
            intelligence_menu()
            break
        elif user_choice == "M":
            monitoring_menu()
            break
        elif user_choice == "A":
            about()
            show_options()
        elif user_choice == "O":
            show_options()
        elif user_choice == "Q":
            quit()
            break


def show_options():
    """
    Prints out the main menu options.
    """

    keys = ["R", "I", "M", "A", "O", "Q"]
    desc = ["access the pollution (R)eporting module", "access the mobility (I)ntelligence module",
            "access the real-time "
            "(M)onitoring module",
            "access the (A)bout text", "show (O)ptions", "(Q)uit the application"]
    print(format_message(" " * 100, color.UNDERLINE, color.YELLOW))
    print(format_message("OPTIONS:", color.UNDERLINE, color.BOLD, color.DARKCYAN))
    for k, d in zip(keys, desc):
        print(f"{format_message(k, color.BOLD, color.BLUE)} - {format_message(d, color.GREEN)}")
    print("\n")


def reporting_menu():
    """
    Handles and prints out the reporting menu.
    """

    print(format_message("Welcome to the Pollution Reporting Module!", color.BOLD, color.UNDERLINE, color.DARKCYAN))
    monitoring_station = choose_station()
    pollutant = choose_pollutant()
    show_reporting_functions()
    data = reporting.load_data()  # Load CSV data
    while True:
        user_choice = input(format_message("Enter an option 1-9: ", color.BOLD, color.PURPLE)).upper()
        if user_choice == "1":  # Daily average
            print(format_message(
                f"Calculating daily average for pollutant {pollutant.upper()} at {monitoring_station}... (2dp)",
                color.BOLD, color.BLUE))
            daily_average = reporting.daily_average(data, monitoring_station, pollutant)
            for day, value in enumerate(daily_average):
                print(format_message(f"Day {day + 1}: ", color.BOLD, color.BLUE) + format_message(
                    f"{round(value, 2) if type(value) == float else value}",
                    color.GREEN))
            show_reporting_functions()
        elif user_choice == "2":  # Daily median
            print(format_message(
                f"Calculating daily median for pollutant {pollutant.upper()} at {monitoring_station}... (2dp)",
                color.BOLD, color.BLUE))
            daily_median = reporting.daily_median(data, monitoring_station, pollutant)
            for day, value in enumerate(daily_median):
                print(format_message(f"Day {day + 1}: ", color.BOLD, color.BLUE) + format_message(
                    f"{round(value, 2) if type(value) == float else value}",
                    color.GREEN))
            show_reporting_functions()
        elif user_choice == "3":  # Hourly average
            print(format_message(
                f"Calculating hourly average for pollutant {pollutant.upper()} at {monitoring_station}... (2dp)",
                color.BOLD, color.BLUE))
            hourly_average = reporting.hourly_average(data, monitoring_station, pollutant)
            for hour, value in enumerate(hourly_average):
                print(format_message(f"{hour}".zfill(2), color.BOLD, color.BLUE) +
                      format_message(":00 : ", color.BOLD, color.BLUE) +
                      format_message(f"{round(value, 2)}", color.GREEN))
            show_reporting_functions()
        elif user_choice == "4":  # Monthly average
            print(format_message(
                f"Calculating monthly average for pollutant {pollutant.upper()} at {monitoring_station}... (2dp)",
                color.BOLD, color.BLUE))
            monthly_average = reporting.monthly_average(data, monitoring_station, pollutant)
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Aug", "Sep", "Oct", "Nov", "Dec"]
            for month, value in zip(months, monthly_average):
                print(format_message(f"{month}: ", color.BOLD, color.BLUE) +
                      format_message(f"{round(value, 2) if type(value) == float else value}", color.GREEN))
            show_reporting_functions()
        elif user_choice == "5":  # Peak value
            date = input(format_message("Enter the date for which you wish to search for the peak value (YYYY-MM-DD): ",
                                        color.BOLD, color.PURPLE))
            print(format_message(
                f"Calculating peak value and hour for pollutant {pollutant.upper()} at {monitoring_station} on {date}... (2dp)",
                color.BOLD, color.BLUE))
            hour, peak_value = reporting.peak_hour_date(data, date, monitoring_station, pollutant)
            print(
                format_message(f"Peak value was at {hour} and the value was ", color.BOLD, color.BLUE) + format_message(
                    f"{round(peak_value, 2)}",
                    color.GREEN))
            show_reporting_functions()
        elif user_choice == "6":  # Calculate missing data
            print(format_message(
                f"Calculating the number of missing entries for pollutant {pollutant.upper()} at {monitoring_station}...",
                color.BOLD, color.BLUE))
            missing_data = reporting.count_missing_data(data, monitoring_station, pollutant)
            print(format_message(f"Number of missing entries: ", color.BOLD, color.BLUE) + format_message(
                f"{round(missing_data, 2)}",
                color.GREEN))
            show_reporting_functions()
        elif user_choice == "7":  # Fill missing data
            new_value = input(
                format_message("Enter the new value to replace missing entries: ", color.BOLD, color.PURPLE))
            print(format_message(
                f"Replacing missing data with {new_value}...",
                color.BOLD, color.BLUE))
            data = reporting.fill_missing_data(data, new_value, monitoring_station, pollutant)
            print(format_message(f"Missing entries replaced with ", color.BOLD, color.BLUE) + format_message(
                f"{new_value}",
                color.GREEN))
            show_reporting_functions()
        elif user_choice == "8":  # Re-choose station and pollutant
            monitoring_station = choose_station()
            pollutant = choose_pollutant()
            show_reporting_functions()
        elif user_choice == "9":  # Go back to main menu
            main_menu()
            break


def show_reporting_functions():
    """
    Prints out reporting function options
    """

    desc = ["Calculate daily average", "Calculate daily median", "Calculate hourly average",
            "Calculate monthly average", "Calculate peak hour", "Count missing data", "Fill missing data",
            "Change monitoring station and pollutant", "Main Menu"]
    show_module_options(desc)


def choose_station():
    """
    Allows user to choose a valid monitoring station.
    Returns:
        A string name of the chosen monitoring station.
    """
    stations = ["Marylebone Road", "Harlington", "N Kensington"]
    for i in range(len(stations)):
        print(f"{format_message(str(i + 1), color.BLUE)} - {format_message(stations[i], color.GREEN)}")
    print("\n")
    while True:
        user_choice = input(format_message("Choose a monitoring station 1-3: ", color.BOLD, color.PURPLE)).upper()
        if user_choice in ["1", "2", "3"]:
            return stations[int(user_choice) - 1]


def choose_pollutant():
    """
    Allows user to choose a valid pollutant.
    Returns:
        A string name of the chosen pollutant.
    """

    pollutants = ["no", "pm10", "pm25"]
    for i in range(len(pollutants)):
        print(f"{format_message(str(i + 1), color.BLUE)} - {format_message(pollutants[i].upper(), color.GREEN)}")
    print("\n")
    while True:
        user_choice = input(format_message("Choose a pollutant 1-3:", color.BOLD, color.PURPLE)).upper()
        if user_choice in ["1", "2", "3"]:
            return pollutants[int(user_choice) - 1]


def intelligence_menu():
    """
    Handles and prints out the intelligence menu.
    """
    print(format_message("Welcome to the Mobility Intelligence Module!", color.BOLD, color.UNDERLINE, color.DARKCYAN))
    show_intelligence_menu_options()
    while True:
        user_choice = input(format_message("Enter an option 1-5: ", color.BOLD, color.PURPLE))
        if user_choice == "1" or user_choice == "2" or user_choice == "3" or user_choice == "4":
            map_filename = input(format_message(
                "Enter map filename (located at data/map_filename): ", color.BOLD, color.PURPLE))
            while not os.path.exists(f"data/{map_filename}"):
                map_filename = input(format_message(
                    "Enter map filename (located at data/map_filename): ", color.BOLD, color.PURPLE))
            upper_threshold = int(input(format_message("Enter upper threshold: ", color.BOLD, color.PURPLE)))
            lower_threshold = int(input(format_message("Enter lower threshold: ", color.BOLD, color.PURPLE)))
            if user_choice == "1":  # Find red pixels
                print(format_message("Finding red pixels...", color.BOLD, color.BLUE))
                intelligence.find_red_pixels(map_filename, upper_threshold=upper_threshold,
                                             lower_threshold=lower_threshold)
                print(
                    f"{format_message('Output stored at', color.BOLD, color.BLUE)} {format_message('map-red-pixels.jpg', color.UNDERLINE, color.BOLD, color.GREEN)}")
            elif user_choice == "2":  # Find cyan pixels
                print(format_message("Finding cyan pixels...", color.BOLD, color.BLUE))
                intelligence.find_cyan_pixels(map_filename, upper_threshold=upper_threshold,
                                              lower_threshold=lower_threshold)
                print(
                    f"{format_message('Output stored at', color.BOLD, color.BLUE)} {format_message('map-cyan-pixels.jpg', color.UNDERLINE, color.BOLD, color.GREEN)}")
            elif user_choice == "3" or user_choice == "4":  # Connected components
                while True:
                    type_connected_component = input(
                        format_message("What colour would you like to calculate the connected components "
                                       "for? (R/C): ", color.BOLD, color.PURPLE)).upper()
                    if type_connected_component == "R":
                        binary_image = intelligence.find_red_pixels(map_filename, upper_threshold=upper_threshold,
                                                                    lower_threshold=lower_threshold)
                        break
                    elif type_connected_component == "C":
                        binary_image = intelligence.find_cyan_pixels(map_filename, upper_threshold=upper_threshold,
                                                                     lower_threshold=lower_threshold)
                        break
                print(format_message("Detecting connected components...", color.BOLD, color.BLUE))
                connected_components = intelligence.detect_connected_components(binary_image)
                if user_choice == "3":  # Connected components unsorted
                    print(
                        f"{format_message('Output stored at', color.BOLD, color.BLUE)} {format_message('cc-output-2a.txt', color.BOLD, color.GREEN)}")
                elif user_choice == "4":  # Connected components sorted
                    intelligence.detect_connected_components_sorted(connected_components)
                    print(
                        f"{format_message('Output stored at', color.BOLD, color.BLUE)} {format_message('cc-output-2b.txt', color.BOLD, color.GREEN)}")
                    print(
                        f"{format_message('Top 2 largest connected components stored at', color.BOLD, color.BLUE)} {format_message('cc-top-2.jpg', color.BOLD, color.GREEN)}")
            show_intelligence_menu_options()
        elif user_choice == "5":  # Back to main menu
            main_menu()
            break


def show_intelligence_menu_options():
    """
    Prints out intelligence menu options.
    """

    desc = ["Find red pixels", "Find cyan pixels", "Detected connected components",
            "Detect connected components sorted", "Main Menu"]
    show_module_options(desc)


def monitoring_menu():
    """
    Handles and prints out the monitoring menu.
    """

    print(format_message("Welcome to the Real-time Monitoring Module!", color.BOLD, color.UNDERLINE, color.DARKCYAN))
    df = monitoring.get_current_pollution_indices()
    show_monitoring_menu_options()
    while True:
        user_choice = input(format_message("Enter an option 1-5: ", color.BOLD, color.PURPLE))
        if user_choice == "1":  # Display site codes
            monitoring.display_site_codes()
            show_monitoring_menu_options()
        elif user_choice == "2":  # Display species codes
            monitoring.display_species()
            show_monitoring_menu_options()
        elif user_choice == "3":  # Display today's trend
            monitoring_station = input(format_message("Enter a valid site code: ", color.BOLD, color.PURPLE))
            monitoring.display_todays_trend(monitoring_station)
            print(
                f"{format_message('Output stored at', color.BOLD, color.BLUE)} {format_message('graph.png', color.UNDERLINE, color.BOLD, color.GREEN)}")
            print(
                format_message('NOTE: Some data may be missing it will not be plotted on the graph for those hours', color.BOLD, color.BLUE))
            show_monitoring_menu_options()
        elif user_choice == "4":  # Display map of pollution
            pollutant = input(format_message("Enter a valid pollutant code: ", color.BOLD, color.PURPLE)).upper()
            monitoring.display_map(df, pollutant)
            print(
                f"{format_message('Output stored at', color.BOLD, color.BLUE)} {format_message('pollution.png', color.UNDERLINE, color.BOLD, color.GREEN)}")
            print(
                format_message('NOTE: Unfilled circles mean that trace amounts were recorded', color.BOLD, color.BLUE))
            show_monitoring_menu_options()
        elif user_choice == "5":  # Display health advice
            monitoring_station = input(format_message("Enter a valid site code: ", color.BOLD, color.PURPLE))
            pollutant = input(format_message("Enter a valid pollutant code: ", color.BOLD, color.PURPLE)).upper()
            try:
                station = df.loc[df["Site Code"] == monitoring_station]
                print(
                    format_message(f"Air Quality Index for site code {monitoring_station}: ", color.BOLD, color.BLUE) +
                    format_message(f"{station[pollutant].values[0]}", color.GREEN))
                monitoring.display_health_advice(int(station[pollutant]))
            except:
                print(format_message(f"No data was collected for site {monitoring_station}", color.BOLD, color.RED))
            finally:
                show_monitoring_menu_options()
        elif user_choice == "6":  # Back to main menu
            main_menu()
            break


def show_monitoring_menu_options():
    """
    Prints out monitoring menu options.
    """

    desc = ["Show stations site codes", "Show species codes", "Display today's pollution trend",
            "Display map of pollution levels", "Display health advice", "Main Menu"]
    show_module_options(desc)


def show_module_options(desc):
    """
    Generic function for printing out module options depending on descriptions passed in.
    Parameters:
        desc (list): List of descriptions for each option.
    """
    for i in range(len(desc)):
        print(f"{format_message(str(i + 1), color.BLUE)} - {format_message(desc[i], color.GREEN)}")
    print("\n")


def about():
    """
    Prints out about information for the program.
    """

    print(format_message("Module Code:", color.UNDERLINE, color.BLUE) + format_message(" ECM1400", color.BOLD,
                                                                                       color.GREEN))
    print(format_message("Candidate Number:", color.UNDERLINE, color.BLUE) + format_message(" 248407", color.BOLD,
                                                                                            color.GREEN))
    print(format_message("Candidate Name:", color.UNDERLINE, color.BLUE) + format_message(" Arjun Modi", color.BOLD,
                                                                                          color.GREEN))


def quit():
    """
    Quits the application.
    """

    print(format_message("Exiting Application...", color.BOLD, color.RED))
    exit()


if __name__ == '__main__':
    main_menu()
