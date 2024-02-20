import requests
from lambdas.services import secrets_service
from lambdas.utils.common import SafeDict
from lambdas.utils.dt_utils import datetime_from_seconds
from lambdas.utils.validators import raise_not_defined


class OpenWeatherService:
    def __init__(self):
        self.api_key = secrets_service.get_secret_value

    def get_weather(self, city):
        raise_not_defined('city', city)
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}',
                                timeout=5)
        response_code = response.status_code
        if response_code != 200:
            raise Exception(f'OpenWeather API failed with {response_code=}')  # pylint:disable=broad-exception-raised
        data = response.json()
        weather = weather_reducer(data)
        return weather


def weather_reducer(weather):
    weather = SafeDict(weather)
    sunrise = datetime_from_seconds(weather.get_nested('sys', 'sunrise')).strftime(
        '%H:%M:%S') if weather.get_nested('sys', 'sunrise') else None
    sunset = datetime_from_seconds(weather.get_nested('sys', 'sunset')).strftime('%H:%M:%S') if weather.get_nested(
        'sys', 'sunset') else None
    return {
        'id': weather.get('id', 0),
        'cityName': weather.get('name'),
        'longitude': weather.get_nested('coord', 'lon'),
        'latitude': weather.get_nested('coord', 'lat'),
        'currentWeather': {
            'status': weather.get_nested('weather', 0, 'main'),
            'description': weather.get_nested('weather', 0, 'description'),
            'temp': weather.get_nested('main', 'temp'),
            'tempHigh': weather.get_nested('main', 'temp_max'),
            'tempLow': weather.get_nested('main', 'temp_min'),
            'pressure': weather.get_nested('main', 'pressure'),
            'humidity': weather.get_nested('main', 'humidity'),
            'windSpeed': weather.get_nested('wind', 'speed')
        },
        'sunrise': sunrise,
        'sunset': sunset
    }
