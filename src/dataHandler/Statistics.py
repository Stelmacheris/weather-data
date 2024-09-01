from datetime import datetime, timedelta
import pytz
import pandas as pd

class Statistics:
    """
    A class to calculate various statistical metrics (e.g., max, min, standard deviation)
    for temperature data for a specific city based on hourly information.

    Attributes:
        city (str): The name of the city for which statistics will be calculated.
        cities_hourly_info (pd.DataFrame): A filtered DataFrame containing hourly temperature 
                                           data for the specified city.
        statistic_info (dict[str, float]): A dictionary to store calculated statistical metrics.
    
    Methods:
        get_today() -> None: Calculates and stores today's max, min, and standard deviation 
                             of temperature for the city.
        get_yesterday() -> None: Calculates and stores yesterday's max, min, and standard deviation 
                                 of temperature for the city.
        get_current_week() -> None: Calculates and stores the current week's max, min, and standard 
                                    deviation of temperature for the city.
        get_7_days() -> None: Calculates and stores the last 7 days' max, min, and standard deviation 
                              of temperature for the city.
        get_today_date() -> datetime.date: Returns today's date.
        get_statistic() -> dict[str, float]: Returns the dictionary of calculated statistical metrics.
    """

    def __init__(self, city: str, hourly_info_df: pd.DataFrame) -> None:
        """
        Initializes the Statistics class with the specified city and hourly information DataFrame.

        Args:
            city (str): The name of the city for which statistics will be calculated.
            hourly_info_df (pd.DataFrame): A DataFrame containing hourly temperature data for multiple cities.
        """
        self.city: str = city
        self.cities_hourly_info: pd.DataFrame = hourly_info_df[hourly_info_df['city'] == self.city]
        self.statistic_info: dict[str, float] = {}

    def get_today(self) -> None:
        """
        Calculates today's max, min, and standard deviation of temperature for the city 
        and stores the results in the statistic_info dictionary.
        """
        self.statistic_info['city_max_today'] = self.cities_hourly_info['temperature'][self.cities_hourly_info['inserted_at'].dt.date == self.get_today_date()].max().item()
        self.statistic_info['city_min_today'] = self.cities_hourly_info['temperature'][self.cities_hourly_info['inserted_at'].dt.date == self.get_today_date()].min().item()
        self.statistic_info['city_std_today'] = self.cities_hourly_info['temperature'][self.cities_hourly_info['inserted_at'].dt.date == self.get_today_date()].std().item()

    def get_yesterday(self) -> None:
        """
        Calculates yesterday's max, min, and standard deviation of temperature for the city 
        and stores the results in the statistic_info dictionary.
        """
        self.statistic_info['city_max_yesterday'] = self.cities_hourly_info['temperature'][self.cities_hourly_info['inserted_at'].dt.date == self.get_today_date() - timedelta(days=1)].max()
        self.statistic_info['city_min_yesterday'] = self.cities_hourly_info['temperature'][self.cities_hourly_info['inserted_at'].dt.date == self.get_today_date() - timedelta(days=1)].min()
        self.statistic_info['city_std_yesterday'] = self.cities_hourly_info['temperature'][self.cities_hourly_info['inserted_at'].dt.date == self.get_today_date() - timedelta(days=1)].std()

    def get_current_week(self) -> None:
        """
        Calculates the current week's max, min, and standard deviation of temperature for the city 
        and stores the results in the statistic_info dictionary.
        """
        self.statistic_info['city_max_last_week'] = self.cities_hourly_info['temperature'][self.cities_hourly_info['inserted_at'].dt.date >= self.get_today_date() - timedelta(days=datetime.now().weekday())].max().item()
        self.statistic_info['city_min_last_week'] = self.cities_hourly_info['temperature'][self.cities_hourly_info['inserted_at'].dt.date >= self.get_today_date() - timedelta(days=datetime.now().weekday())].max().item()
        self.statistic_info['city_std_last_week'] = self.cities_hourly_info['temperature'][self.cities_hourly_info['inserted_at'].dt.date >= self.get_today_date() - timedelta(days=datetime.now().weekday())].max().item()

    def get_7_days(self) -> None:
        """
        Calculates the last 7 days' max, min, and standard deviation of temperature for the city 
        and stores the results in the statistic_info dictionary.
        """
        self.statistic_info['city_max_last_7_days'] = self.cities_hourly_info['temperature'][self.cities_hourly_info['inserted_at'].dt.date >= self.get_today_date() - timedelta(days=7)].max().item()
        self.statistic_info['city_min_last_7_days'] = self.cities_hourly_info['temperature'][self.cities_hourly_info['inserted_at'].dt.date >= self.get_today_date() - timedelta(days=7)].min().item()
        self.statistic_info['city_std_last_7_days'] = self.cities_hourly_info['temperature'][self.cities_hourly_info['inserted_at'].dt.date >= self.get_today_date() - timedelta(days=7)].std().item()

    def get_today_date(self) -> datetime.date:
        """
        Returns today's date.

        Returns:
            datetime.date: The current date.
        """
        return datetime.now().date()

    def get_statistic(self) -> dict[str, float]:
        """
        Returns the dictionary of calculated statistical metrics.

        Adds today's date to the statistic_info dictionary and returns it.

        Returns:
            dict[str, float]: The dictionary containing the calculated statistics for the city, 
                              including today's date.
        """
        self.statistic_info['date_inserted'] = self.get_today_date().strftime('%Y-%m-%d')
        return self.statistic_info
