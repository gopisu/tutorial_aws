from gql.dsl import DSLSchema, DSLQuery

from aws_utils import get_gql_client, query_gql


def test_get_weather_status(ctx):
    city = 'London'
    client = get_gql_client(ctx=ctx)
    ds: DSLSchema = DSLSchema(client.schema)
    query = DSLQuery(
        ds.Query.weather().select(
            ds.Weather.status,
        )
    )

    result = query_gql(client=client, query=query)
    print(result)
    assert result['weather']['status'] == 'OK'
