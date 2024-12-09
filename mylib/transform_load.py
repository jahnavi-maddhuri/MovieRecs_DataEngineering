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
                    release_date STRING,
                    title STRING,
                    vote_average DOUBLE,
                    vote_count INT,
                    genre_names STRING
                )
            """
            )
        c.execute("SELECT * from movie_recs_final")
        result = c.fetchall()
        if not result:

            for _, row in df.iterrows():
                genre_ids_str = (
                    ",".join(map(str, row["genre_ids"].split(",")))
                    if "genre_ids" in row
                    else ""
                )
                genre_names_str = (
                    ",".join(map(str, row["genre_names"].split(",")))
                    if "genre_names" in row
                    else ""
                )

                # Prepare parameters for insertion
                params = (
                    bool(row["adult"]),
                    row["backdrop_path"],
                    genre_ids_str,
                    int(row["id"]),
                    row["original_language"],
                    row["original_title"],
                    float(row["popularity"]),
                    row["poster_path"],
                    row["release_date"],
                    row["title"],
                    float(row["vote_average"]),
                    int(row["vote_count"]),
                    genre_names_str,
                )

                # Use parameterized queries to safely insert data
                c.execute(
                    """
                    INSERT INTO movie_recs_final (
                        adult, 
                        backdrop_path, 
                        genre_ids, 
                        id, 
                        original_language, 
                        original_title, 
                        popularity, 
                        poster_path, 
                        release_date, 
                        title, 
                        vote_average, 
                        vote_count, 
                        genre_names
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    params,
                )
        c.close()
    print("successfully loaded data into Databricks")
    return "success"


if __name__ == "__main__":
    load()
