import json
import logging as log
import os
from typing import Generator

import boto3
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.appsync_auth import AppSyncJWTAuthentication, AppSyncApiKeyAuthentication
from gql.transport.appsync_websockets import AppSyncWebsocketsTransport

from tests.integration.conftest import TestContext
from lambdas.utils import gql_utils
from lambdas.utils.common import Singleton
from lambdas.utils.gql_utils import query_gql

from gql import gql, Client


class AWSUtils(metaclass=Singleton):

    def __init__(self, ctx: TestContext):
        self.ctx = ctx
        self.session = boto3.Session(profile_name="serverless")
        self.lambda_client = self.session.client(
            "lambda",
            endpoint_url=ctx.endpoint_url,
            region_name=ctx.region
        )
        self.cognito_client = self.session.client(
            "cognito-idp",
            endpoint_url=ctx.endpoint_url,
            region_name=ctx.region
        )

        log.info("CURRENT DIR: %s", os.getcwd())

        if os.path.isdir('lambdas'):
            base_path = ''
        elif os.path.isdir('../lambdas'):
            base_path = '../'
        else:
            base_path = '../../'

        log.info("PATH: %s", base_path)

        self.schema = gql_utils.get_graphql_schema(base_path=base_path)
        log.info(f"""Effective Schema:
        
        {self.schema}
        
        """)

    def call_lambda(self, payload: dict, function_name: str):
        json_payload = json.dumps(payload)
        resp = self.lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json_payload)
        if resp.get('StatusCode', None) == 200:
            return json.loads(resp['Payload'].read().decode("utf-8"))

        raise Exception(f"Call to lambda {function_name} failed")

    def destroy(self):
        self.ctx = None
        self.session = None
        self.lambda_client = None
        AWSUtils._instances = {}


def get_gql_client(ctx: TestContext) -> Client:
    auth = AppSyncApiKeyAuthentication(
        host=ctx.host,
        api_key=ctx.api_key
    )

    transport = AIOHTTPTransport(url=ctx.graphql_url, auth=auth)
    aws = AWSUtils(ctx=ctx)
    return Client(transport=transport, fetch_schema_from_transport=False, schema=aws.schema, execute_timeout=20)


def do_gql(ctx: TestContext, query):
    client = get_gql_client(ctx)
    return query_gql(client=client, query=query)


def subscribe(query: str, ctx: TestContext, params: dict = None) -> Generator:
    auth = AppSyncJWTAuthentication(
        host=ctx.host
    )
    transport = AppSyncWebsocketsTransport(
        url=ctx.graphql_ws, auth=auth, connect_timeout=60, close_timeout=60, ack_timeout=60)

    client = Client(transport=transport,
                    fetch_schema_from_transport=False,
                    schema=AWSUtils(ctx=ctx).schema,
                    execute_timeout=60
                    )

    return client.subscribe(gql(query), variable_values=params)
