from flask import Flask, render_template, request,url_for,redirect
import requests
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
app.debug = True  # Enable debug mode for detailed error messages

# Define the API key and URL
API_KEY = "f3de2559-77f3-45e2-94c2-03206d30180d"

# Cache file path
CACHE_FILE = "air_quality_cache.json"

def fetch_data(city, state):
    """Fetch data from the API based on city and state."""
    url = f"http://api.airvisual.com/v2/city?city={city}&state={state}&country=USA&key={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_cached_data(city,state):
    """Retrieve cached data if it's less than 24 hours old; otherwise, fetch new data."""
   
    # Fetch new data and update the cache
    data = fetch_data(city,state)
    with open(CACHE_FILE, "w") as f:
        json.dump({"timestamp": datetime.now().isoformat(), "data": data}, f)
    return data

@app.route("/home", methods=['GET', 'POST'])
def home():
    city = request.args.get('city')
    state = request.args.get('state')
    print(city)
    try:
        data = get_cached_data(city,state)
        
        if data.get("status") == "success":
            # Extract air quality information
            city = data['data']['city']
            state = data['data']['state']
            country = data['data']['country']
            current_aqi = data['data']['current']['pollution']['aqius']
            current_temp = data['data']['current']['weather']['tp']
            current_humidity = data['data']['current']['weather']['hu']
            current_pressure = data['data']['current']['weather']['pr']
            timestamp = data['data']['current']['weather']['ts']
            
            # Format the timestamp to a readable format
            current_temp = current_temp * (9/5) + 32  # Convert to Fahrenheit
            formatted_datetime = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%B %d, %Y")
            
            # Render the HTML template with real data for the first item and placeholder data for the rest
            return render_template("index2.html", city=city, state=state, country=country, current_aqi=current_aqi,
                                   current_temp=current_temp, current_humidity=current_humidity,
                                   current_pressure=current_pressure, timestamp=formatted_datetime)
        else:
            return render_template("index2.html", error="Error: Data not available at this time.")

    except requests.exceptions.RequestException:
        return render_template("index2.html", error="Error: Unable to connect to the air quality service.")
    except Exception as e:
        return render_template("index2.html", error=f"An unexpected error occurred: {e}")

@app.route("/", methods=['GET', 'POST'])
def search_form():
    if request.method == 'POST':
        print("State:", request.form.get('state'))
        print("City:", request.form.get('city'))
    
        state = request.form.get('state')
        city = request.form.get('city')
        
       
        return redirect(url_for('home', city=city, state=state))
    
   
    return render_template("index.html", city="Buffalo", state="New York")

if __name__ == "__main__":
    app.run()
