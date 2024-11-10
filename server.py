from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

# Define the API key and URL
API_KEY = "f3de2559-77f3-45e2-94c2-03206d30180d"
url = f"http://api.airvisual.com/v2/city?city=Buffalo&state=New York&country=USA&key={API_KEY}"

# Cache file path
CACHE_FILE = "air_quality_cache.json"

def fetch_data():
    response = requests.get(url)
    response.raise_for_status()
    return response.json()



@app.route("/", methods=['GET', 'POST'])
def search_form():
    if request.method == 'POST':
        state = request.form.get('state')
        city = request.form.get('city')
        return redirect(url_for('home', city=city, state=state))
    
    return render_template("index.html")
@app.route("/home", methods=['GET', 'POST'])
def home():
    try:
        data = get_cached_data()
        
        if data.get("status") == "success":
            city = data['data']['city']
            state = data['data']['state']
            country = data['data']['country']
            current_aqi = data['data']['current']['pollution']['aqius']
            current_temp = data['data']['current']['weather']['tp']
            current_humidity = data['data']['current']['weather']['hu']
            current_pressure = data['data']['current']['weather']['pr']
            timestamp = data['data']['current']['weather']['ts']
            
            
            current_temp = current_temp*(9/5)+ 32
            formatted_datetime =  datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%B %d, %Y")
          
            return render_template("index2.html", city=city, state=state, country=country, current_aqi=current_aqi,
                                   current_temp=current_temp, current_humidity=current_humidity,
                                   current_pressure=current_pressure, timestamp=formatted_datetime)
        else:
            return render_template("index2.html", error="Error: Data not available at this time.")

    except requests.exceptions.RequestException:
        return render_template("index2.html", error="Error: Unable to connect to the air quality service.")
    except Exception as e:
        return render_template("index2.html", error=f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    app.run()