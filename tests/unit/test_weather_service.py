import os

import pytest
import responses
from lambdas.services.weather_service import OpenWeatherService
from lambdas.utils.validators import ValidationException


@responses.activate
def test_get_weather(mocker):
    # Arrange
    mocker.patch('lambdas.services.weather_service.secrets_service.get_secret_value', return_value='weather_api_key')
    responses.add(
        responses.GET,
        'http://api.openweathermap.org/data/2.5/weather?q=London&appid=weather_api_key',
        json={"coord": {"lon": -0.1257, "lat": 51.5085},
              "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04n"}],
              "base": "stations",
              "main": {"temp": 50.58, "feels_like": 49.23, "temp_min": 48.69, "temp_max": 52, "pressure": 1022,
                       "humidity": 83}, "visibility": 10000, "wind": {"speed": 11.5, "deg": 240},
              "clouds": {"all": 100}, "dt": 1708456939,
              "sys": {"type": 2, "id": 2075535, "country": "GB", "sunrise": 1708412767, "sunset": 1708449769},
              "timezone": 0, "id": 2643743, "name": "London", "cod": 200},
        status=200
    )
    service = OpenWeatherService()

    # Act
    result = service.get_weather('London')

    # Assert
    assert result == {
        'id': 2643743,
        'cityName': 'London',
        'longitude': -0.1257,
        'latitude': 51.5085,
        'currentWeather': {
            'status': 'Clouds',
            'description': 'overcast clouds',
            'temp': 50.58,
            'tempHigh': 52,
            'tempLow': 48.69,
            'pressure': 1022,
            'humidity': 83,
            'windSpeed': 11.5
        },
        'sunrise': '07:06:07',
        'sunset': '17:22:49'
    }


def test_get_weather_invalid_city(mocker):
    # Arrange
    os.environ['AWS_REGION'] = 'us-west-2'  # Set the environment variable
    mocker.patch('lambdas.services.weather_service.secrets_service.get_secret_value', return_value='weather_api_key')
    service = OpenWeatherService()

    # Act & Assert
    with pytest.raises(ValidationException):
        service.get_weather(None)
