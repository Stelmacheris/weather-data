from src.dataHandler.PydanticData.Model.models import WeatherData

def return_fields(json):
    data = WeatherData(**json) 
    return data.weather[0].description,data.main.temp,data.weather[0].id