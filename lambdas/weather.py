from lambdas import init_lambda
import logging
from lambdas.services.weather_service import OpenWeatherService

init_lambda()
LOG = logging.getLogger(__name__)

def handler(_event, _context):
    service = OpenWeatherService()
    LOG.debug(f'Event: {_event}')
    city_name = _event.get('arguments').get('cityName')
    return service.get_weather(city_name)
