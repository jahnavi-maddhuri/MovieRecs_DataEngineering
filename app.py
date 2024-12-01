from flask import Flask, request, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Birthdate Fun Fact</title>
</head>
<body>
    <h1>Enter Your Details</h1>
    <form method="POST" action="/">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required><br><br>
        <label for="birthdate">Birthdate (YYYY-MM-DD):</label>
        <input type="text" id="birthdate" name="birthdate" required><br><br>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def say_hello():
    if request.method == "POST":
        # Get data from form submission
        name = request.form.get("name")
        birthdate = request.form.get("birthdate")
        try:
            # Parse birthdate
            birth_date_obj = datetime.strptime(birthdate, "%Y-%m-%d")
            month = birth_date_obj.month
            day = birth_date_obj.day
        except ValueError:
            return "Invalid date format! Please use YYYY-MM-DD."

        # Fetch fun fact
        fact_url = f"http://numbersapi.com/{month}/{day}/date"
        try:
            response = requests.get(fact_url)
            if response.status_code == 200:
                fun_fact = response.text
            else:
                fun_fact = "Could not retrieve a fun fact at this time."
        except Exception as e:
            fun_fact = f"Error fetching fun fact: {e}"

        # Return response
        return f"<h1>Hi {name}!</h1><p>Here's a fun fact about your birthdate:<br>{fun_fact}</p>"

    # Show the input form
    return render_template_string(HTML_TEMPLATE)


if __name__ == "__main__":
    app.run(debug=True)
