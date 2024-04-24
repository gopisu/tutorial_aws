from lambdas import init_lambda
from lambdas.services.weather_service import OpenWeatherService

init_lambda()


def handler(_event, _context):
    service = OpenWeatherService()
    city_name = _event.get('arguments').get('cityName')
    return service.get_weather(city_name)
