import reporting


def test_load_data():
    """
    Tests if all 3 CSVs are loaded into the dictionary.
    """

    data = reporting.load_data()
    assert len(data.keys()) == 3


def test_daily_average():
    """
    Tests for 365 entries for all stations and pollutants.
    """

    data = reporting.load_data()
    for key, value in data.items():
        for pollutant in ["no", "pm10", "pm25"]:
            if len(reporting.daily_average(data, key, pollutant)) != 365:
                assert False
    assert True


def test_daily_median():
    """
    Tests for 365 entries for all stations and pollutants.
    """

    data = reporting.load_data()
    for key, value in data.items():
        for pollutant in ["no", "pm10", "pm25"]:
            if len(reporting.daily_median(data, key, pollutant)) != 365:
                assert False
    assert True


def test_hourly_average():
    """
    Tests for 24 entries for all stations and pollutants.
    """

    data = reporting.load_data()
    for key, value in data.items():
        for pollutant in ["no", "pm10", "pm25"]:
            if len(reporting.hourly_average(data, key, pollutant)) != 24:
                assert False
    assert True


def test_monthly_average():
    """
    Tests for 12 entries for all stations and pollutants.
    """

    data = reporting.load_data()
    for key, value in data.items():
        for pollutant in ["no", "pm10", "pm25"]:
            if len(reporting.monthly_average(data, key, pollutant)) != 12:
                assert False
    assert True


def test_peak_hour_date():
    """
    Tests for the correct peak hour and value for specified date.
    """

    data = reporting.load_data()
    date = "2021-01-01"
    assert reporting.peak_hour_date(data, date, "Harlington", "no") == ("20:00", 13.00595)


def test_count_missing_data():
    """
    Tests that correct number of missing data values are counted.
    """

    data = reporting.load_data()
    assert reporting.count_missing_data(data, "Harlington", "no") == 70


def test_fill_missing_data():
    """
    Tests that the fill missing data function correctly fills missing data.
    """

    data = reporting.load_data()
    filled_data = reporting.fill_missing_data(data, 0, "Harlington", "no")
    assert reporting.count_missing_data(filled_data, "Harlington", "no") == 0
