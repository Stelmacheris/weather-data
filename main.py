from src.database.PostgresConnection import PostgresConnection
import pandas as pd
from sqlalchemy.engine import Engine

pc: PostgresConnection = PostgresConnection()
engine: Engine = pc.get_engine()

with engine.connect() as conn:
    cities = pd.read_sql(
     sql="SELECT city FROM public.city",
        con=conn.connection
    )

cities: list[str] = cities['city'].tolist()

with engine.connect() as conn:
    hourly_info_df = pd.read_sql(
        sql="""SELECT A.*,B.city FROM public.hourly_weather A
            INNER JOIN public.city B
            ON A.city_id = B.id
        """,
        con=conn.connection
    )