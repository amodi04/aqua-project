# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification.
# 
# This module will access data from the LondonAir Application Programming Interface (API)
# The API provides access to data to monitoring stations. 
# 
# You can access the API documentation here http://api.erg.ic.ac.uk/AirQuality/help
#
import pandas as pd
import requests
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import xml.etree.ElementTree as ET
from utils import color, format_message
import datetime
import numpy as np


def get_data(site_code='MY1', species_code='NO', start_date=None, end_date=None):
    """
    Gets the data for a specified site code and species code in a date range.
    Parameters:
        site_code (str): The site code for which to get the data for.
        species_code (str): The species code for which to get the data for.
        start_date (str): The starting date for which the data range is applicable for.
        end_date (str): The end date for which the data is applicable for.
    """

    start_date = datetime.date.today() if start_date is None else start_date  # Use today if no start date passed in
    end_date = (start_date + datetime.timedelta(
        days=1)) if end_date is None else end_date  # Use the next date after the start data if no end date passed in

    url = f"https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
    res = requests.get(url)
    return res.json()


def display_site_codes():
    """
    Displays the list of site codes and site names along with their local authorities
    """

    site_codes = get_site_codes(False)  # Get dictionary of local authorities and their site codes
    for k, v in site_codes.items():
        print(format_message(k, color.UNDERLINE, color.BLUE, color.BOLD))  # Print local authority
        for i, j in v.items():
            print("    {:<40} ".format(i) + format_message(j, color.GREEN))  # Print name of site and site code


def get_site_codes(pos, authority=True):
    """
    Gets the site codes and returns in different formats depending on parameters.
    Parameters:
        pos (bool): Flag used to check whether to return site locations along with codes.
        authority (bool): Flag used to check whether to return authority along with codes.
    """

    url = "https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/GroupName=London/Json"
    res = requests.get(url)
    sites = res.json()["Sites"]["Site"]  # Get list of sites
    if authority:  # Sites added under local authorities to give user more information on sites
        site_codes = {}
        for site in sites:
            site_codes[site["@LocalAuthorityName"]] = {}  # Create all keys for each local authority
        for site in sites:
            if site["@SiteName"] == "- National Physical Laboratory, Teddington":
                area = site["@SiteName"][2:]  # National Physical Laboratory name formatted wrongly in API so checks
                # made in order for output to be correct
            else:
                area = site["@SiteName"]
            if pos:
                site_codes[site["@LocalAuthorityName"]][area] = (
                    site["@SiteCode"],
                    [site["@Longitude"], site["@Latitude"]])  # Adds positional data along with site code
            else:
                site_codes[site["@LocalAuthorityName"]][area] = site["@SiteCode"]
        return site_codes
    else:
        site_codes = []
        for site in sites:
            if pos:
                site_codes.append([site["@SiteCode"], site["@Longitude"],
                                   site["@Latitude"]])  # Adds positional data along with site code
            else:
                site_codes.append([site["@SiteCode"]])
        return site_codes


def display_todays_trend(site_code):
    """
    Creates a graph plotting all pollution data for the current day for a specific site code.
    Parameters:
        site_code (str): The site for which to plot data for.
    """

    for species_code in get_species():
        today_data = get_data(site_code, species_code)  # Get data for each pollutant
        y = []
        for measurement in today_data["RawAQData"]["Data"]:
            value = measurement["@Value"]
            if value == "":
                y.append(np.nan)  # No data for this hour so use np.nan as matplotlib will not plot data for this value
            else:
                y.append(float(value))
        plt.plot([f"{i}".zfill(2) + ":00" for i in range(len(y))], y)  # Plot data against time

    plt.xticks(fontsize='x-small', rotation=90)
    plt.xlabel("Time")
    plt.ylabel("Pollution Concentration (µg/m^3)")
    plt.legend(get_species(), loc='upper right')
    plt.savefig("graph.png")
    plt.close()  # Clear plot from memory ready for other figures which may be created


def get_current_pollution_indices():
    """
    Gets air quality indices for all stations that have recorded in the last hour.
    Returns:
        A pandas DataFrame of all the stations that have recorded data for each pollutant.
    """

    data = []
    species = get_species()
    count = 0
    sites = get_site_codes(False, authority=False)  # Gets list of site codes
    for site in sites:
        site_code = site[0]
        url = f"https://api.erg.ic.ac.uk/AirQuality/Hourly/MonitoringIndex/SiteCode={site_code}/Json"
        res = requests.get(url)
        json = res.json()
        if json is not None:  # If station has recorded data
            row = ["0" for _ in range(7)]  # Initialise empty row with 7 columns
            site_data = json["HourlyAirQualityIndex"]["LocalAuthority"]["Site"]
            row[0] = site_data["@SiteCode"]  # Site code at first column
            if type(site_data[
                        "species"]) is list:  # Check if data for species is contained in a list in the json.
                # Sometimes the API returns a dictionary instead
                for i in site_data["species"]:
                    for j in range(len(species)):
                        if i["@SpeciesCode"] == species[j]:
                            row[j] = i["@AirQualityIndex"]
            else:
                for j in range(len(species)):
                    if site_data["species"]["@SpeciesCode"] == species[j]:
                        row[j] = site_data["species"]["@AirQualityIndex"]
            data.append(row)
        count += 1
        print(f"Processed {count} / {len(sites)} sites")
    columns = ["Site Code"]
    for i in species:
        columns.append(i)
    df = pd.DataFrame(data, columns=columns)  # Create dataframe from data
    print(format_message(f"{len(df.index)} / {len(sites)}", color.BOLD, color.BLUE) + format_message(
        " stations collected data for the last hour", color.GREEN))
    return df


def get_position(site_code):
    """
    Gets the longitude and latitude position for a given monitoring station.
    Parameters:
        site_code (str): The site for which to get the positional data for.
    Returns:
        A tuple of the longitude and latitude data for the site.
    """

    site_codes = get_site_codes(True, authority=False)
    for site, longitude, latitude in site_codes:  # Search for station and return the positional data
        if site == site_code:
            return longitude, latitude


def display_map(df, pollutant):
    """
    Plots pollution data on a map of london give a pollutant and air quality indices.
    Parameters:
        df (pandas.DataFrame): The dataframe of pollution indices for each site that has recorded data.
        pollutant (str): The pollutant for which to plot the data for.
    """

    fig, ax = plt.subplots(1)  # Create a pyplot figure
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Remove surrounding borders
    img = plt.imread("data/london.png")  # Read in map of london
    ax.imshow(img)  # Load image into figure
    num_sites = len(df.index)
    for i, row in enumerate(df.index):
        site_code = df["Site Code"][row]
        pol_val = int(df[pollutant][row])
        long, lat = get_position(site_code)
        x, y = translate_to_pixel(long, lat, img.shape)  # Translate longitude and latitude data into pixel coordinates
        ax.add_patch(
            Circle((x, y), 2 + (5 * pol_val), fill=bool(pol_val), color=(min(float(1), 1 / 5 * pol_val), 0.01,
                                                                         0.01)))  # Plot circle with larger radius
        # and more red for larger amounts of pollution
        print(f"Plotted {i + 1} / {num_sites} sites")
    plt.gca().set_axis_off()  # Remove axis
    plt.savefig("pollution.png", dpi=1200)  # Save image
    plt.close()  # Clear pyplot memory


def translate_to_pixel(longitude, latitude, img_shape):
    """
    Calculates pixel coordinates on an image given the position data.
    Parameters:
        longitude (str): The longitude position of the station.
        latitude (str): The latitude position of the station.
        img_shape (tuple): The dimensions for the image
    Returns:
        A tuple of x and y coordinates for the pixel.
    """

    height = img_shape[0]  # Get height bounds of image
    width = img_shape[1]  # Get width bounds of image
    try:
        # Numbers are constants given by the bounding box of the image of london. This is used to calculate pixel
        # components. Note: This will only work for data/london.png
        x = round((float(longitude) - (-0.5555)) * width / (0.2980 + 0.5555))  # Get linear translation of x component
        y = round((float(latitude) - 51.2555) * height / (51.7245 - 51.2555))  # Get linear translation of y component
        return x, y
    except TypeError:
        return 0, 0  # If no valid positional data was given for a site


def get_species(code_only=True):
    """
    Gets all valid species codes.
    Parameters: code_only (bool): Flag used to specify if name of species should also
    be included in the output of this function. Returns: A list of species codes.
    """

    url = "https://api.erg.ic.ac.uk/AirQuality/Information/Species/Json"
    res = requests.get(url)
    json = res.json()
    if code_only:
        return [species["@SpeciesCode"] for species in json["AirQualitySpecies"]["Species"]]
    return [(species["@SpeciesName"], species["@SpeciesCode"]) for species in
            json["AirQualitySpecies"]["Species"]]  # Tuple of name and species code in list


def display_species():
    """
    Prints out species code and their names.
    """

    species = get_species(code_only=False)
    for name, code in species:
        print("{:<20} ".format(name) + format_message(code, color.GREEN))  # Print in tabular format


def get_index_health_advice():
    """
    Gets the index health advice for each band.
    Returns:
        A pandas Dataframe containing information for each band of index health.
    """

    url = "https://api.erg.ic.ac.uk/AirQuality/Information/IndexHealthAdvice"  # Get XML data because the JSON
    # endpoint is not valid (problem with API)
    res = requests.get(url)
    xml = res.content.decode("utf-8")  # Decode into utf-8 character encoding
    root = ET.fromstring(xml)  # Turn into an ElementTree
    health_advice = []
    for i in range(len(root)):
        health_advice.append([root[i].attrib, root[i][0].attrib, root[i][
            1].attrib])  # Append air quality band and health advice for each type of population
    df = pd.DataFrame(columns=["Band", "Lower", "Upper", "At-risk", "General"])
    for i in health_advice:  # Split information into further sub categories
        band = i[0]
        band_name = band["AirQualityBand"]
        lower_index = band["LowerAirQualityIndex"]
        upper_index = band["UpperAirQualityIndex"]
        at_risk_advice = i[1]["Advice"]
        general_advice = i[2]["Advice"]
        df = pd.concat([pd.DataFrame([[band_name, lower_index, upper_index, at_risk_advice, general_advice]],
                                     columns=df.columns), df], ignore_index=True)  # Add data to dataframe
    return df


def display_health_advice(index):
    """
    Display health advice given an air quality index.
    Parameters:
        index (int): The index for which to display health advice for.
    """

    df = get_index_health_advice()
    desc = ["Air Quality Band", "Lower Air Quality Index", "Higher Air Quality Index", "At-risk individuals Health "
                                                                                       "Advice", "General population "
                                                                                                 "Health Advice"]
    if index == 0:  # No advice for index 0
        print(format_message("No health advice for pollution index 0 as either no pollution has been recorded, "
                             "or there are only trace amounts", color.BOLD, color.GREEN))
        return

    for i in df.index:
        if int(df["Lower"][i]) <= index <= int(df["Upper"][i]):
            for j, k in enumerate(df.keys()):
                print(format_message(desc[j], color.BOLD, color.UNDERLINE, color.DARKCYAN))
                print(format_message(df[k][i], color.RED))
