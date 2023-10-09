from flask import Flask, jsonify, render_template
from amadeus import Client

app = Flask(__name__)

CLIENT_ID = 't0RuoeMPg4KjA5d6BcEJxI8g7w8nESpr'
CLIENT_SECRET = 'vQI5LkDvzAhqae3C'

# Initialize the Amadeus Client
amadeus = Client(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    hostname='test'  # use 'production' for production environment
)


@app.route('/get-activities/<latitude>/<longitude>', methods=['GET'])
def get_activities(latitude, longitude):
    response = amadeus.shopping.activities.get(latitude=latitude, longitude=longitude)

    if response.status_code == 200:
        return jsonify(response.data)
    else:
        return jsonify({"message": "Error fetching data from Amadeus API", "error": response.data})


@app.route('/')
def index():
    # For demonstration purposes, using predefined latitude and longitude.
    activities_response = amadeus.shopping.activities.get(latitude="40.41436995", longitude="-3.69170868")
    
    # Log the response for debugging purposes
    print("Amadeus API Response:", activities_response.data)

    # Assuming the response structure is a list of activities directly (this might need adjustment based on actual structure)
    activities = activities_response.data if activities_response.status_code == 200 else []

    return render_template("index.html", activities=activities)


if __name__ == "__main__":
    app.run(debug=True)
