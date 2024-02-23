import datetime

from gql.dsl import DSLSchema, DSLQuery

from aws_utils import get_gql_client, query_gql


def test_get_weather_one_field(ctx):
    cityName = 'London'
    client = get_gql_client(ctx=ctx)
    ds: DSLSchema = DSLSchema(client.schema)
    query = DSLQuery(
        ds.Query.weather(cityName=cityName).select(
            ds.Weather.sunrise(),
        )
    )

    weather_dict = query_gql(client=client, query=query)
    assert isinstance(weather_dict, dict), "Input should be a dictionary"
    assert 'weather' in weather_dict, "Dictionary should have 'weather' key"
    assert isinstance(weather_dict['weather'], dict), "'weather' value should be a dictionary"
    assert 'sunrise' in weather_dict['weather'], "'weather' dictionary should have 'sunrise' key"
    assert isinstance(weather_dict['weather']['sunrise'], str), "'sunrise' value should be a string"

    # Check time format
    try:
        datetime.datetime.strptime(weather_dict['weather']['sunrise'], '%H:%M:%S')
    except ValueError:
        raise AssertionError("Incorrect time format, should be 'HH:MM:SS'")


def test_get_weather_all_fields(ctx):
    cityName = 'London'
    client = get_gql_client(ctx=ctx)
    ds: DSLSchema = DSLSchema(client.schema)
    query = DSLQuery(
        ds.Query.weather(cityName=cityName).select(
            ds.Weather.zip(),
            ds.Weather.cityName(),
            ds.Weather.longitude(),
            ds.Weather.latitude(),
            ds.Weather.sunrise(),
            ds.Weather.sunset(),
            ds.Weather.currentWeather.select(
                ds.CurrentWeather.status(),
                ds.CurrentWeather.description(),
                ds.CurrentWeather.temp(),
                ds.CurrentWeather.feelsLike(),
                ds.CurrentWeather.tempHigh(),
                ds.CurrentWeather.tempLow(),
                ds.CurrentWeather.pressure(),
                ds.CurrentWeather.humidity(),
                ds.CurrentWeather.windSpeed(),
            )
        )
    )
    weather_dict = query_gql(client=client, query=query)
    assert_structure_and_type(weather_dict)


def assert_structure_and_type(weather_dict):
    assert isinstance(weather_dict, dict), "Input should be a dictionary"
    assert 'weather' in weather_dict, "Dictionary should have 'weather' key"
    assert isinstance(weather_dict['weather'], dict), "'weather' value should be a dictionary"

    weather = weather_dict['weather']
    expected_keys = ['zip', 'cityName', 'longitude', 'latitude', 'sunrise', 'sunset', 'currentWeather']
    for key in weather.keys():
        assert key in expected_keys, f"Unexpected key '{key}' in 'weather' dictionary"

    assert isinstance(weather['currentWeather'], dict), "'currentWeather' value should be a dictionary"
    expected_current_weather_keys = ['status', 'description', 'temp', 'feelsLike', 'tempHigh', 'tempLow', 'pressure',
                                     'humidity', 'windSpeed']
    for key in weather['currentWeather'].keys():
        assert key in expected_current_weather_keys, f"Unexpected key '{key}' in 'currentWeather' dictionary"


def test_pet(ctx):
    petDetails = {
        "id": '1',
        "type": 'dog',
        "price": "123.45"
    }

    client = get_gql_client(ctx=ctx)
    ds: DSLSchema = DSLSchema(client.schema)

    mutation = DSLMutation(
        ds.Mutation.createPet(input=petDetails).select(
            ds.Pet.id(),
            ds.Pet.type(),
            ds.Pet.price(),
        )
    )

    result = client.execute(mutation)
    print(result)
