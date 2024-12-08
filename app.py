from flask import Flask, request, render_template_string
import requests
from datetime import datetime
from mylib.queries import query  # import query functions that we make

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


@app.route("/", methods=["GET", "POST"])
# I think based on what the user inputs, we call our query functions using probably variables based on what the user requests. then get the output of the query and display it here?
def say_hello():
    if request.method == "POST":
        # Get data from form submission
        genre = request.form.get("genre")
        mood = request.form.get("mood")
        name = request.form.get("name")
        try:
            # Parse birthdate
            result = query(genre, mood)
        except ValueError:
            return "Invalid genre/does not exist"

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
    app.run(debug=True)
