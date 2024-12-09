import pandas as pd
import numpy as np
import os
import requests

pd.set_option("mode.copy_on_write", True)


# 47400
def extract(file_path="data/movies.csv", directory="data", token=os.getenv("token")):

    movie_pd = pd.DataFrame()
    for page in range(1, 500):
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page}&sort_by=popularity.desc"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
        }

        response = requests.get(url, headers=headers)
        results = response.json()["results"]
        results_pd = pd.DataFrame(results)
        movie_pd = pd.concat([movie_pd, results_pd], ignore_index=True)

    genres = [
        {"id": 28, "name": "Action"},
        {"id": 12, "name": "Adventure"},
        {"id": 16, "name": "Animation"},
        {"id": 35, "name": "Comedy"},
        {"id": 80, "name": "Crime"},
        {"id": 99, "name": "Documentary"},
        {"id": 18, "name": "Drama"},
        {"id": 10751, "name": "Family"},
        {"id": 14, "name": "Fantasy"},
        {"id": 36, "name": "History"},
        {"id": 27, "name": "Horror"},
        {"id": 10402, "name": "Music"},
        {"id": 9648, "name": "Mystery"},
        {"id": 10749, "name": "Romance"},
        {"id": 878, "name": "Science Fiction"},
        {"id": 10770, "name": "TV Movie"},
        {"id": 53, "name": "Thriller"},
        {"id": 10752, "name": "War"},
        {"id": 37, "name": "Western"},
    ]

    genre_dict = {genre["id"]: genre["name"] for genre in genres}
    movie_pd["genre_names"] = movie_pd["genre_ids"].apply(
        lambda ids: [genre_dict[id] for id in ids]
    )

    if not os.path.exists(directory):
        os.makedirs(directory)
    movie_pd.to_csv(file_path, index=False)
    return file_path


if __name__ == "__main__":
    extract()
