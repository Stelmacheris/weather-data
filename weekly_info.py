from datetime import datetime, timedelta
from main import engine, hourly_info_df
from hourly_info import get_highest_lowest_temp
from statistic import get_info_by_date, fetch_rain_count
import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("weekly_statistics.log"),
        logging.StreamHandler()
    ]
)

async def main():
    logging.info("Starting weekly statistics processing")
    
    current_time = datetime.now().replace(microsecond=0)
    logging.info(f"Current time: {current_time}")
    
    last_week = datetime.now().date() - timedelta(datetime.now().weekday())
    logging.info(f"Last week's starting date: {last_week}")
    
    high_low_df = get_highest_lowest_temp(current_time, hourly_info_df, last_week, True)
    logging.info("Saving weekly high and low temperature data to the database")
    await asyncio.to_thread(high_low_df.to_sql, name='weekly_high_low', con=engine, if_exists='append', index=False)

    today = datetime.now().date()
    last_weekday = datetime.now().date() - timedelta(days=datetime.now().weekday())
    logging.info(f"Last weekday date: {last_weekday}")
    
    last_week_df = get_info_by_date(hourly_info_df, last_weekday, True)
    logging.info(f"Retrieved {len(last_week_df)} records for last week's data")

    rain_df = fetch_rain_count(last_week_df)
    logging.info(f"Found {len(rain_df)} records with rain-related descriptions")
    
    rain_df = rain_df.groupby('city_id').size().reset_index(name='hourly_count')
    rain_df['inserted_at'] = today
    logging.info("Saving weekly rain information to the database")
    await asyncio.to_thread(rain_df.to_sql, name='weekly_rain_info', con=engine, if_exists='append', index=False)

    logging.info("Weekly statistics processing completed")

asyncio.run(main())
