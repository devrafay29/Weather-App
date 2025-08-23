from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)
with open ("config.json" , "r") as c:
    param = json.load(c) ["params"]

API_KEY = param["key"]
BASE_URL = param["url"]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html" , param = param)

@app.route("/weather", methods=["GET", "POST"])
def weather():
    city = request.form["city"]

    if not city.strip():
        return render_template("index.html", param = param, weather=None, error="Please enter a city name.")

    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if str(data.get("cod")) != "200":
            error_message = data.get("message", "An error occurred.")
            return render_template("index.html", weather=None, error=error_message.capitalize() , param = param)

        weather = {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "temp_min": data["main"]["temp_min"],
            "temp_max": data["main"]["temp_max"],
            "description": data["weather"][0]["description"].capitalize(),
            "icon_url": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        }

        return render_template("index.html", weather=weather , param = param)

    except requests.RequestException:
        return render_template("index.html", weather=None, error="Failed to connect to weather service.")

if __name__ == '__main__':
    app.run(debug=True)
