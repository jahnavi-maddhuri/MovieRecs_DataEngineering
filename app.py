from flask import Flask, request, render_template_string
import requests
import os
from databricks import sql

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
        <label for="genre">Genre:</label>
        <input type="text" id="genre" name="genre" required><br><br>
        <label for="keyword">Any keywords?</label>
        <input type="text" id="keyword" name="keyword" required><br><br>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def say_hello():
    if request.method == "POST":
        # Get data from form submission
        genre = request.form.get("genre")
        keyword = request.form.get("keyword")
        try:
            with sql.connect(server_hostname = os.getenv("SERVER_HOSTNAME"),
                 http_path       = os.getenv("DATABRICKS_HTTPPATH"),
                 access_token    = os.getenv("DATABRICKS_KEY")) as conn:
                with conn.cursor() as cursor:
                    query = """
                    SELECT original_title, vote_average
                    FROM movies
                    WHERE overview LIKE ? AND genre=?
                    ORDER BY vote_average DESC
                    LIMIT 3;
                    """
                    cursor.execute(query, (f"%{keyword}%", genre))

                    # Fetch results
                    results = cursor.fetchall()
                    return render_template_string(
                            "<h2>Top Movies:</h2><ul>" +
                            "".join(f"<li>{row[0]}</li>" for row in results) +
                            "</ul>"
                        )

        except Exception as e:
            return "Unable to fetch results"


if __name__ == "__main__":
    app.run(debug=True)
