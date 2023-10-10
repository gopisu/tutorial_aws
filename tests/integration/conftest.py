import logging as log
from dataclasses import dataclass

import boto3
import pytest

from services import secrets_service
from utils.common import LogManager, init_json_serialisation


@dataclass
class TestContext:
    region: str
    endpoint_url: str
    graphql_url: str
    graphql_ws: str
    host: str
    api_key: str


def get_graphql_api(api_list_response: dict):
    api_list = api_list_response['graphqlApis']
    for api in api_list:
        if api['name'] == 'efi-serverless-local-graphql':
            return api['apiId'], api['uris']['GRAPHQL'], api['uris']['REALTIME']

    raise Exception("GraphQL API endpoint not found")


def get_api_key(profile: str, endpoint_url):
    arn = secrets_service.find_secret_arn(name='API-key-secret', region='us-east-1', profile=profile, endpoint_url=endpoint_url)
    return secrets_service.get_secret(arn, region='us-east-1', profile=profile, endpoint_url=endpoint_url)


@pytest.fixture(scope="session", autouse=True)
def ctx():
    # os.environ['DB_APP_SECRET'] = """{\"dbClusterIdentifier\":\"local-db-cluster\",
    #     \"password\":\"example\",
    #     \"dbname\":\"example\",
    #     \"engine\":\"postgres\",
    #     \"port\":5432,
    #     \"host\":\"localhost\",
    #     \"username\":\"example\"}"""

    log_manager = LogManager()
    log_manager.init_logging(log_level=log.DEBUG)

    init_json_serialisation()

    endpoint_url = "http://localhost:4566"
    region = "us-east-1"
    session = boto3.Session(profile_name="serverless")
    client = session.client("appsync", endpoint_url=endpoint_url, region_name=region)

    api_id, graphql_url, ws_url = get_graphql_api(client.list_graphql_apis())
    if not (graphql_url.startswith('http://') or graphql_url.startswith('https://')):
        raise Exception(f"Invalid URL {graphql_url}")

    if not (ws_url.startswith('ws://') or graphql_url.startswith('wss://')):
        raise Exception(f"Invalid Websocket URL {ws_url}")

    host = graphql_url.split('/')[2]
    api_key = get_api_key(profile="serverless", endpoint_url=endpoint_url)

    return TestContext(
        region=region,
        endpoint_url=endpoint_url,
        graphql_url=graphql_url,
        graphql_ws=ws_url,
        host=host,
        api_key=api_key
    )
