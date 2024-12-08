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

    if not os.path.exists(directory):
        os.makedirs(directory)
    movie_pd.to_csv(file_path, index=False)
    return file_path


if __name__ == "__main__":
    extract()
