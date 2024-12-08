"""Query the database"""

import os
from databricks import sql
from dotenv import load_dotenv

complex_query = """"""  # Thinking we do something that would depend on what the user inputs / requests
# order by popularity of vote average by default? or maybe release date?


def query(a_query):
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
        c.execute(a_query)
        result = c.fetchall()
        print("Query Output: \n")
        print(result)
        c.close()
    return "Successfully queried"
