from src.dataHandler.Statistics import Statistics
import pandas as pd
from main import engine, cities, hourly_info_df
from hourly_info import get_highest_lowest_temp
from datetime import datetime, timedelta
import asyncio
from src.dataHandler.ApiData import ApiData
from typing import Union
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("city_statistics.log"),
        logging.StreamHandler()
    ]
)

def fetch_rain_count(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Fetching rain count data.")
    words_to_find: list[str] = ['rain', 'thunderstorm', 'drizzle']
    mask = df['description'].str.contains('|'.join(words_to_find), case=False, na=False)
    rain_count_df = df[mask]
    logging.info(f"Found {len(rain_count_df)} entries with rain-related weather descriptions.")
    return rain_count_df

def get_info_by_date(hourly_info_df: pd.DataFrame, date_to_check: datetime.date, is_weekly: bool = False) -> pd.DataFrame:
    logging.info(f"Retrieving information for date: {date_to_check}. Weekly data: {is_weekly}")
    if is_weekly:
        df: pd.DataFrame = hourly_info_df[hourly_info_df['inserted_at'].dt.date >= date_to_check]
    else:
        df = hourly_info_df[hourly_info_df['inserted_at'].dt.date == date_to_check]
    logging.info(f"Retrieved {len(df)} records for the specified date range.")
    return df

async def process_city_statistics(city: str, index: int, hourly_info_df: pd.DataFrame) -> dict:
    logging.info(f"Processing statistics for city: {city}")
    city_statistic: Statistics = Statistics(city, hourly_info_df)
    await asyncio.to_thread(city_statistic.get_today)
    await asyncio.to_thread(city_statistic.get_yesterday)
    await asyncio.to_thread(city_statistic.get_current_week)
    await asyncio.to_thread(city_statistic.get_7_days)
    cs: dict = await asyncio.to_thread(city_statistic.get_statistic)
    cs['city_id'] = index + 1
    logging.info(f"Completed processing statistics for city: {city}")
    return cs

async def main() -> None:
    logging.info("Starting main process")
    current_time: datetime = datetime.now().replace(microsecond=0)
    
    tasks = [process_city_statistics(city, index, hourly_info_df) for index, city in enumerate(cities)]
    cities_statistics: list[dict] = await asyncio.gather(*tasks)

    cities_statistics_df: pd.DataFrame = pd.DataFrame(cities_statistics)
    logging.info("Saving city statistics to the database")
    await asyncio.to_thread(cities_statistics_df.to_sql, name='statistic', con=engine, if_exists='append', index=False)

    today: datetime.date = datetime.now().date()
    logging.info("Calculating and saving highest and lowest temperature data")
    high_low_df: pd.DataFrame = get_highest_lowest_temp(current_time, hourly_info_df, today)
    await asyncio.to_thread(high_low_df.to_sql, name='day_high_low', con=engine, if_exists='append', index=False)

    logging.info("Fetching and saving rain-related data")
    today_df: pd.DataFrame = get_info_by_date(hourly_info_df, today)
    rain_df: pd.DataFrame = fetch_rain_count(today_df)
    rain_df = rain_df.groupby('city_id').size().reset_index(name='hourly_count')
    rain_df['inserted_at'] = today
    await asyncio.to_thread(rain_df.to_sql, name='daily_rain_info', con=engine, if_exists='append', index=False)

    logging.info("Main process completed")

asyncio.run(main())
