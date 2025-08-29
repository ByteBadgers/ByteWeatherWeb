from flask import Flask, render_template, request
from weather import get_weather, get_forecast
import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    city = "Austin"
    if request.method == "POST":
        city = request.form.get("city", "Austin")

    weather = get_weather(city)
    forecast = get_forecast(city)
    timestamp = datetime.datetime.now().strftime("%I:%M %p")

    return render_template("index.html", weather=weather, forecast=forecast, timestamp=timestamp)

if __name__ == "__main__":
    app.run(debug=True)
