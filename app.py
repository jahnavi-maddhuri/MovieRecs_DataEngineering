from flask import Flask, request, render_template_string # import query functions that we make
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

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Movie Request Form</title>
</head>
<body>
    <h1>Enter Your Details</h1>
    <form method="POST" action="/">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required><br><br>
        <label for="genre">Genre:</label>
        <input type="text" id="genre" name="genre" required><br><br>
        <label for="mood">Mood:</label>
        <input type="text" id="mood" name="mood" required><br><br>
        <button type="submit">Submit</button>
    </form>
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
                    FROM movies
                    WHERE overview LIKE ? AND genre_ids=?
                    ORDER BY vote_average DESC
                    LIMIT 3;
                    """ 
            c.execute(a_query, (f"%{mood}%", genre))
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
                movies = "<br>".join([f"{movie[0]} (Rating: {movie[1]})" for movie in result])
            else:
                movies = "No movies found"
            #Return result
            return f"<h1>Hi {name}!</h1><p>Here are your movie recommendations:<br>{movies}</p>"
        except Exception as e:
            return f"<h1>Error:</h1><p>{e}</p>"

        # Fetch fun fact
        '''fact_url = f"http://numbersapi.com/{month}/{day}/date"
        try:
            response = requests.get(fact_url)
            if response.status_code == 200:
                fun_fact = response.text
            else:
                fun_fact = "Could not retrieve a fun fact at this time."
        except Exception as e:
            fun_fact = f"Error fetching fun fact: {e}"'''

        # Return response
        return f"<h1>Hi {name}!</h1><p>Here's your movie rec:<br>{result}</p>"

    # Show the input form
    return render_template_string(HTML_TEMPLATE)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80,debug=True)
