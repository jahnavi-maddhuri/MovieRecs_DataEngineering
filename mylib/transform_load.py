from dotenv import load_dotenv
from databricks import sql
import pandas as pd
import os


def load(dataset="data/movies.csv"):
    """Transforms and Loads data into the local databricks database"""
    df = pd.read_csv(dataset, delimiter=",", skiprows=1)
    load_dotenv()
    server_h = os.getenv("SERVER_HOSTNAME")
    access_token = os.getenv("ACCESS_TOKEN")
    # http_path = os.getenv("HTTP_PATH")
    with sql.connect(
        server_hostname=server_h,
        http_path="/sql/1.0/warehouses/2d6f41451e6394c0",
        access_token=access_token,
    ) as connection:
        c = connection.cursor()
        c.execute("SHOW TABLES FROM default LIKE 'movie_recs*'")
        result = c.fetchall()

        if not result:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS movie_recs_final (
                    adult BOOLEAN,
                    backdrop_path STRING,
                    genre_ids STRING,
                    id INT,
                    original_language STRING,
                    original_title STRING,
                    popularity DOUBLE,
                    poster_path STRING,
                    release_date STRING
                    title STRING,
                    vote_average DOUBLE,
                    vote_count INT
                )
            """
            )
        c.execute("SELECT * from movie_recs_final")
        result = c.fetchall()
        if not result:

            for _, row in df.iterrows():
                convert = tuple(row)
                c.execute(f"INSERT INTO movie_recs_final VALUES {convert}")
        c.close()
    print("successfully loaded data into Databricks")
    return "success"


if __name__ == "__main__":
    load()
