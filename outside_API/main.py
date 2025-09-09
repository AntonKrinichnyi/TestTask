import json
from csv import DictWriter

import requests
from requests.exceptions import RequestException

url = "https://jsonplaceholder.typicode.com/users"
fieldnames = ["id", "name", "email"]

try:
    response = requests.get(url=url)
    data = response.json()
except RequestException as e:
    print(f"Request failure {e}")


with open("outside_API/data.csv", "w", newline="", encoding="utf-8") as file:
    writer = DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows([{"id": d["id"], "name": d["name"], "email": d["email"]} for d in data])

print("Data loaded successfuly")