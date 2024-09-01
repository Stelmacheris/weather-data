import pandas as pd
from datetime import datetime, timedelta
from src.database.PostgresConnection import PostgresConnection
from src.dataHandler.ApiData import ApiData
from src.dataHandler.PydanticData.DataTransformation.DataTransformation import return_fields
from main import engine, cities, hourly_info_df
import asyncio
import subprocess
from typing import Dict, Any
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("weather_data.log"),
        logging.StreamHandler()
    ]
)

async def fetch_city_data(city: str, index: int, current_time: datetime) -> Dict[str, Any]:
    logging.info(f"Fetching data for city: {city}")
    apiData: ApiData = ApiData(city)
    data: dict = await asyncio.to_thread(apiData.get_weather_now)
    description: str
    temperature: float
    _ = return_fields(data)
    description, temperature, _ = return_fields(data)
    logging.info(f"Fetched data for city: {city}, temperature: {temperature}, description: {description}")
    return {
        "city_id": index + 1,
        "temperature": temperature,
        "description": description,
        "inserted_at": current_time
    }

def get_highest_lowest_temp(current_time: datetime, all_city_data_df: pd.DataFrame, date_to_equal: datetime.date, is_weekly: bool = False) -> pd.DataFrame:
    logging.info(f"Calculating highest and lowest temperatures for date: {date_to_equal}")
    max_hour_temperature: float
    min_hour_temperature: float
    if is_weekly:
        max_hour_temperature = all_city_data_df['temperature'][all_city_data_df['inserted_at'].dt.date >= date_to_equal].max()
        min_hour_temperature = all_city_data_df['temperature'][all_city_data_df['inserted_at'].dt.date >= date_to_equal].min()
    else:
        max_hour_temperature = all_city_data_df['temperature'][all_city_data_df['inserted_at'].dt.date == date_to_equal].max()
        min_hour_temperature = all_city_data_df['temperature'][all_city_data_df['inserted_at'].dt.date == date_to_equal].min()
    
    high_df: pd.Series = all_city_data_df[['city_id', 'temperature']][all_city_data_df['temperature'] == max_hour_temperature].iloc[0]
    low_df: pd.Series = all_city_data_df[['city_id', 'temperature']][all_city_data_df['temperature'] == min_hour_temperature].iloc[0]
    
    high_low_df: pd.DataFrame = pd.DataFrame({
        'date_inserted': [current_time],
        'highest_temp_city_id': [int(high_df['city_id'])],
        'lowest_temp_city_id': [int(low_df['city_id'])],
        'highest_temp': [high_df['temperature']],
        'lowest_temp': [low_df['temperature']]
    })
    logging.info(f"Calculated highest and lowest temperatures: {high_df['temperature']} (City ID: {high_df['city_id']}), {low_df['temperature']} (City ID: {low_df['city_id']})")
    return high_low_df

async def main() -> None:
    current_time: datetime = datetime.now().replace(microsecond=0)
    logging.info("Starting data fetching process")
    tasks = [fetch_city_data(city, index, current_time) for index, city in enumerate(cities)]
    all_city_data: list[Dict[str, Any]] = await asyncio.gather(*tasks)

    all_city_data_df: pd.DataFrame = pd.DataFrame(all_city_data)
    logging.info("Saving all city data to the database")
    await asyncio.to_thread(all_city_data_df.to_sql, name='hourly_weather', con=engine, if_exists='append', index=False)

    today: datetime.date = datetime.now().date()
    logging.info("Calculating and saving highest and lowest temperature data")
    high_low_df: pd.DataFrame = get_highest_lowest_temp(current_time, all_city_data_df, today)
    await asyncio.to_thread(high_low_df.to_sql, name='hourly_high_low', con=engine, if_exists='append', index=False)

    logging.info("Data processing completed")

asyncio.run(main())
