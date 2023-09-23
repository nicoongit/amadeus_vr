from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

AMADEUS_BASE_URL = "https://test.api.amadeus.com/v1"
CLIENT_ID = "XXXX"  # Replace with your client id
CLIENT_SECRET = "XXXX"  # Replace with your client secret


def get_access_token():
    auth_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(auth_url, headers=headers, data=data)
    return response.json().get("access_token")


@app.route('/get-activities/<latitude>/<longitude>', methods=['GET'])
def get_activities(latitude, longitude):
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(
        f"{AMADEUS_BASE_URL}/shopping/activities?latitude={latitude}&longitude={longitude}&radius=1",
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"message": "Error fetching data from Amadeus API"}


@app.route('/')
def index():
    # For demonstration purposes, using predefined latitude and longitude.
    activities = get_activities("40.41436995", "-3.69170868")
    return render_template("index.html", activities=activities)


if __name__ == "__main__":
    app.run(debug=True)
