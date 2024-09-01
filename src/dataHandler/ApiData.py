import requests
import os
from dotenv import load_dotenv
from typing import Any, Dict

load_dotenv()

class ApiData:
    """
    A class to fetch weather data for a given city using the OpenWeatherMap API.

    Attributes:
        city (str): The name of the city for which to fetch weather data.

    Methods:
        get_weather_now() -> Dict[str, Any]:
            Fetches the current weather data for the specified city from the OpenWeatherMap API.
    """

    def __init__(self, city: str) -> None:
        """
        Initializes the ApiData class with the specified city.

        Args:
            city (str): The name of the city for which to fetch weather data.
        """
        self.city: str = city

    def get_weather_now(self) -> Dict[str, Any]:
        """
        Fetches the current weather data for the specified city.

        This method sends a GET request to the OpenWeatherMap API to retrieve 
        the current weather data for the city specified during initialization.

        Returns:
            Dict[str, Any]: A dictionary containing the current weather data 
            returned by the API, including temperature, weather description, 
            humidity, etc.
        """
        base_url: str = "https://api.openweathermap.org/data/2.5/weather"
        base_params: Dict[str, str] = {
            "q": self.city,
            "appid": os.getenv('APP_ID', ''),
            "units": "metric"
        }
        response: requests.Response = requests.get(base_url, base_params)
        results: Dict[str, Any] = response.json()
        return results
