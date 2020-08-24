import json

from yahoo_weather.weather import YahooWeather
from yahoo_weather.config.units import Unit


class Weather:

    def __init__(self, yahoo_weather_api_json):

        self.yahoo_weather_api_json = yahoo_weather_api_json

        self.yahoo_weather_creds_dict = json.load(open(self.yahoo_weather_api_json))

        self.api_connection = self.get_api_connection()

    def get_api_connection(self):
        return YahooWeather(
            APP_ID=self.yahoo_weather_creds_dict["app_id"],
            api_key=self.yahoo_weather_creds_dict["client_id"],
            api_secret=self.yahoo_weather_creds_dict["client_secret"]
        )

    def get_response(self, city="hoboken"):
        self.api_connection.get_yahoo_weather_by_city(city, Unit.fahrenheit)

        ret_str = "{} forecast: currently {} and {}\n--------------".format(
            city.title(),
            self.api_connection.condition.temperature,
            self.api_connection.condition.text
        )

        for forecast in self.api_connection.get_forecasts()[:5]:
            ret_str += "\n   {}: ({} high, {} low) {}".format(
                forecast.day, forecast.high, forecast.low, forecast.text
            )

        return ret_str
