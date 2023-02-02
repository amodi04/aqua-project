import os
import pandas as pd
import monitoring


def test_get_data():
    """
    Tests that the correct data is returned for a specified date range.
    """

    res = monitoring.get_data(start_date="2022-12-10", end_date="2022-12-11")
    assert res == {"RawAQData": {"@SiteCode": "MY1", "@SpeciesCode": "NO",
                                 "Data": [{"@MeasurementDateGMT": "2022-12-10 00:00:00", "@Value": "111.4"},
                                          {"@MeasurementDateGMT": "2022-12-10 01:00:00", "@Value": "82.8"},
                                          {"@MeasurementDateGMT": "2022-12-10 02:00:00", "@Value": "69.9"},
                                          {"@MeasurementDateGMT": "2022-12-10 03:00:00", "@Value": "52.9"},
                                          {"@MeasurementDateGMT": "2022-12-10 04:00:00", "@Value": "37.9"},
                                          {"@MeasurementDateGMT": "2022-12-10 05:00:00", "@Value": "46.6"},
                                          {"@MeasurementDateGMT": "2022-12-10 06:00:00", "@Value": "51.3"},
                                          {"@MeasurementDateGMT": "2022-12-10 07:00:00", "@Value": "77"},
                                          {"@MeasurementDateGMT": "2022-12-10 08:00:00", "@Value": "92.4"},
                                          {"@MeasurementDateGMT": "2022-12-10 09:00:00", "@Value": "95.7"},
                                          {"@MeasurementDateGMT": "2022-12-10 10:00:00", "@Value": "97.4"},
                                          {"@MeasurementDateGMT": "2022-12-10 11:00:00", "@Value": "99.1"},
                                          {"@MeasurementDateGMT": "2022-12-10 12:00:00", "@Value": "141.3"},
                                          {"@MeasurementDateGMT": "2022-12-10 13:00:00", "@Value": "106"},
                                          {"@MeasurementDateGMT": "2022-12-10 14:00:00", "@Value": "84.5"},
                                          {"@MeasurementDateGMT": "2022-12-10 15:00:00", "@Value": "102.5"},
                                          {"@MeasurementDateGMT": "2022-12-10 16:00:00", "@Value": "94.5"},
                                          {"@MeasurementDateGMT": "2022-12-10 17:00:00", "@Value": "82.5"},
                                          {"@MeasurementDateGMT": "2022-12-10 18:00:00", "@Value": "83.6"},
                                          {"@MeasurementDateGMT": "2022-12-10 19:00:00", "@Value": "78.1"},
                                          {"@MeasurementDateGMT": "2022-12-10 20:00:00", "@Value": "66"},
                                          {"@MeasurementDateGMT": "2022-12-10 21:00:00", "@Value": "109.7"},
                                          {"@MeasurementDateGMT": "2022-12-10 22:00:00", "@Value": "113.4"},
                                          {"@MeasurementDateGMT": "2022-12-10 23:00:00", "@Value": "104"}]}}


def test_get_site_codes():
    """
    Tests that all site codes have a site code, longitude and latitude when pos = True
    """

    site_codes = monitoring.get_site_codes(pos=True, authority=False)
    for i in site_codes:
        if len(i) != 3:
            assert False
    assert True


def test_todays_trend():
    """
    Tests that the output file is created.
    """

    monitoring.display_todays_trend("MY1")
    assert os.path.exists("graph.png")


def test_get_pollution_indices():
    """
    Tests that retrieved data is put into a valid data frame.
    """

    assert type(monitoring.get_current_pollution_indices()) == pd.DataFrame


def test_get_position():
    """
    Tests the position retrieved for a site is correct.
    """

    assert monitoring.get_position("MY1") == ("-0.15459", "51.52254")


def test_display_map():
    """
    Tests that the output file is created.
    """

    df = monitoring.get_current_pollution_indices()
    monitoring.display_map(df, "NO2")
    assert os.path.exists("pollution.png")


def test_translate_to_pixel():
    """
    Tests that the given position is translated correctly into pixel coordinates.
    """

    assert monitoring.translate_to_pixel("-0.15459", "51.52254", (878, 995)) == (467, 500)


def test_get_species():
    """
    Tests that retrieved data gives a code and name for each species.
    """

    species_codes = monitoring.get_species(code_only=False)
    for i in species_codes:
        if len(i) != 2:
            assert False
    assert True


def test_get_index_health_advice():
    """
    Tests that all 4 health bands are retrieved.
    """

    df = monitoring.get_index_health_advice()
    assert len(df) == 4