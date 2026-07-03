from pprint import pprint
import requests
from dateutil.parser import parse


class MetaWeatherForecast:
    """
    Simple forecast client for the MetaWeather API.
    TODO: handle network and response exceptions.
    """
    _api_endpoint = "https://www.metaweather.com/api/location/"

    def __init__(self):
        self._cache = {}

    def _get_city_id(self, name):
        resp = requests.get(
            f"{self.__class__._api_endpoint}search/?query={name}"
        ).json()
        return resp[0]["woeid"]

    def get(self, city):
        if city in self._cache:
            print("Retrieving data from cache...")
            return self._cache[city]

        print("Sending HTTP request to the MetaWeather API endpoint...")
        city_id = self._get_city_id(city)
        resp = requests.get(f"{self.__class__._api_endpoint}{city_id}/").json()

        forecast = []
        for daily_data in resp["consolidated_weather"]:
            forecast.append(
                {
                    "date": parse(daily_data["applicable_date"]),
                    "max_temp": daily_data["max_temp"],
                }
            )
        self._cache[city] = forecast
        return forecast


class CityInfo:
    def __init__(self, city, weather_forecast_client=None):
        self.city = city
        self._weather_forecast_client = weather_forecast_client or MetaWeatherForecast()

    def weather_forecast(self):
        return self._weather_forecast_client.get(self.city)


def _main():
    metaweather_client = MetaWeatherForecast()  # for using caching mechanizm
    for _ in range(0, 10):
        city_info = CityInfo("Moscow", weather_forecast_client=metaweather_client)
        forecast = city_info.weather_forecast()
    pprint(forecast)


if __name__ == "__main__":
    _main()
