from pydantic import BaseModel
from typing import List,Union

class Sys(BaseModel):
    country: str
    sunrise: int
    sunset: int

class Clouds(BaseModel):
    all:int

class Wind(BaseModel):
    speed: float
    deg: int

class Main(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: float
    humidity: float
    sea_level: float
    grnd_level: float

class Coord(BaseModel):
    lon: float
    lat: float

class Weather(BaseModel):
    id: int
    main: str
    description: str
    icon: str

class WeatherData(BaseModel):
    coord: Coord
    weather: List[Weather]
    base: str
    main: Main
    visibility: int
    wind: Wind
    clouds: Clouds
    dt: int
    sys: Sys
    timezone: int
    id: int
    name: str
    cod: int
