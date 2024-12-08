import pandas as pd
import numpy as np

pd.set_option("mode.copy_on_write", True)

movie_pd = pd.DataFrame()
# 47400
import requests

for page in range(1, 500):
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page}&sort_by=popularity.desc"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3Y2ExYmI0YTBiZWVjMDM2NDQ2NzIyODVjM2NlZmQ4NyIsIm5iZiI6MTczMjU1NTcxMy41OTksInN1YiI6IjY3NDRiM2MxNDYyNjBlMTRmYmViNDY0YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.pFlTFCibT564k7T9kL4uduJLB-piLv33Lcw-n0yL5LA",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        results = response.json().get("results", [])
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error fetching page {page}: {e}")
    continue

movie_pd.to_csv("movies.csv")