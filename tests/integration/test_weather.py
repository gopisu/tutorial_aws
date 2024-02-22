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
            ds.Weather.id(),
            ds.Weather.cityName(),
            ds.Weather.longitude(),
            ds.Weather.latitude(),
            ds.Weather.sunrise(),
            ds.Weather.sunset(),
        )
    )
    weather_dict = query_gql(client=client, query=query)
    assert isinstance(weather_dict, dict), "Input should be a dictionary"


def get_field_names(schema, typename):
    type_ = schema.get_type(typename)
    return [f.name.value for f in type_.fields]
