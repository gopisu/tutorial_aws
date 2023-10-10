from gql.dsl import DSLSchema, DSLQuery

from aws_utils import get_gql_client, query_gql


def test_get_user_status(ctx):

    client = get_gql_client(ctx=ctx)
    ds: DSLSchema = DSLSchema(client.schema)
    query = DSLQuery(
        ds.Query.status().select(
            ds.Status.status,
            ds.Status.dataSize
        )
    )

    result = query_gql(client=client, query=query)
    assert result['status']['status'] == 'OK'
    assert result['status']['dataSize'] == 0
