import requests
import json
from flask import Flask, render_template

url = "http://api.airvisual.com/v2/countries?key={{7ef89689-3a6a-444f-8439-67151c651cac}}"

payload={}
files={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload, files=files)

print(response.text)




app = Flask(__name__)

@app.route("/")
def home():
    return render_template("./index2.html")
    
if __name__ == "__main__":
    app.run()