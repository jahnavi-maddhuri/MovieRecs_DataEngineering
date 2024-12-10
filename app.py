from flask import (
    Flask,
    request,
    render_template_string,
)  # import query functions that we make
from dotenv import load_dotenv
import os

import traceback

try:
    import databricks.sql as sql
except Exception as e:
    print("Error while importing databricks.sql:")
    print(e)
    traceback.print_exc()


app = Flask(__name__)

RESULT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Movie Recommendations</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Noto Sans', sans-serif;
            background-color: #feffdf;
            color: #668ba4;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .results-container {
            background-color: #dde0ab;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            padding: 20px;
            width: 400px;
            text-align: center;
        }

        h1 {
            color: #668ba4;
            margin-bottom: 20px;
        }

        ul {
            list-style-type: none;
            padding: 0;
        }

        li {
            background-color: #97cba9;
            color: #feffdf;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
        }

        button {
            margin-top: 20px;
            background-color: #668ba4;
            color: #feffdf;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background-color: #97cba9;
        }
    </style>
</head>
<body>
    <div class="results-container">
        <h1>Hi {{ name }}!</h1>
        <p>Here are your movie recommendations:</p>
        <ul>
            {% for movie in movies %}
                <li>{{ movie[0] }} (Rating: {{ movie[1] }})</li>
            {% endfor %}
        </ul>
        <form action="/" method="get">
            <button type="submit">Back to Form</button>
        </form>
    </div>
</body>
</html>
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Movie Request Form</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Noto Sans', sans-serif;
            background-color: #feffdf;
            color: #668ba4;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .form-container {
            background-color: #dde0ab;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            padding: 20px;
            width: 300px;
            text-align: center;
        }

        h1 {
            color: #668ba4;
            margin-bottom: 20px;
        }

        label {
            font-weight: bold;
            display: block;
            margin: 10px 0 5px;
        }

        input, select, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #668ba4;
            border-radius: 5px;
            font-size: 16px;
        }

        input:focus, select:focus, button:focus {
            outline: none;
            border-color: #97cba9;
        }

        button {
            background-color: #97cba9;
            color: #feffdf;
            cursor: pointer;
            font-weight: bold;
        }

        button:hover {
            background-color: #668ba4;
            color: #feffdf;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <h1>Movie Request Form</h1>
        <form method="POST" action="/">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>

            <label for="genre">Genre:</label>
            <select id="genre" name="genre" required>
                <option value="" disabled selected>Select a genre</option>
                <option value="Action">Action</option>
                <option value="Adventure">Adventure</option>
                <option value="Animation">Animation</option>
                <option value="Comedy">Comedy</option>
                <option value="Crime">Crime</option>
                <option value="Documentary">Documentary</option>
                <option value="Drama">Drama</option>
                <option value="Family">Family</option>
                <option value="Fantasy">Fantasy</option>
                <option value="History">History</option>
                <option value="Horror">Horror</option>
                <option value="Music">Music</option>
                <option value="Mystery">Mystery</option>
                <option value="Romance">Romance</option>
                <option value="Science Fiction">Science Fiction</option>
                <option value="TV Movie">TV Movie</option>
                <option value="Thriller">Thriller</option>
                <option value="War">War</option>
                <option value="Western">Western</option>
            </select>

            <label for="mood">Mood:</label>
            <input type="text" id="mood" name="mood" required>

            <button type="submit">Submit</button>
        </form>
    </div>
</body>
</html>

"""


def query(genre, mood):
    load_dotenv()
    server_h = os.getenv("SERVER_HOSTNAME")
    access_token = os.getenv("ACCESS_TOKEN")
    # http_path = os.getenv("HTTP_PATH")
    with sql.connect(
        server_hostname=server_h,
        http_path="/sql/1.0/warehouses/2d6f41451e6394c0",
        access_token=access_token,
    ) as connection:
        with connection.cursor() as c:
            a_query = """
                    SELECT original_title, vote_average
                    FROM movie_recs
                    WHERE overview LIKE ? AND genre_names LIKE ?
                    ORDER BY vote_average DESC
                    LIMIT 3;
                    """
            c.execute(a_query, (f"%{mood}%", f"%{genre}%"))
            result = c.fetchall()
            print("Query Output: \n")
            print(result)
            c.close()
    return result


# I think based on what the user inputs, we call our query functions using probably variables based on what the user requests. then get the output of the query and display it here?
@app.route("/", methods=["GET", "POST"])
def say_hello():
    if request.method == "POST":
        genre = request.form.get("genre")
        mood = request.form.get("mood")
        name = request.form.get("name")
        # Get data from form submission
        try:
            # Parse birthdate
            # Thinking we do something that would depend on what the user inputs / requests
            # order by popularity of vote average by default? or maybe release date?
            result = query(genre, mood)
            if result:
                movies = result
            else:
                movies = [("No movies found", "N/A")]
            # Return result
            return render_template_string(RESULT_TEMPLATE, name=name, movies=movies)
        except Exception as e:
            return f"<h1>Error:</h1><p>{e}</p>"


    # Show the input form
    return render_template_string(HTML_TEMPLATE)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
