import json
import logging as log
import base64
import os

import boto3


class SecretsException(Exception):
    pass


def find_secret_arn(name: str,
                    region: str = None,
                    profile: str = None,
                    endpoint_url: str = None):
    session = boto3.session.Session(profile_name=profile)
    client = session.client(
        service_name='secretsmanager',
        region_name=region,
        endpoint_url=endpoint_url
    )

    filters = [
        {
            'Key': 'name',
            'Values': [name]
        },
    ] if name is not None else []

    secrets = client.list_secrets(
        IncludePlannedDeletion=False,
        MaxResults=100,
        SortOrder='asc',
        Filters=filters
    )

    secrets_list = secrets['SecretList']
    secrets_count = len(secrets_list)
    if secrets_count != 1:
        raise SecretsException(f"Bad search for secrets arn. Got {secrets_count} results for name {name}")

    return secrets_list[0]['ARN']


def get_secret_value(name: str,
                     result_type=str):
    log.debug("Fetching secret value for %s", name)
    env_var_name = name.upper().replace('-', '_')
    env_value = os.environ.get(env_var_name, None)
    if env_value is not None:
        if result_type == dict:
            return json.loads(env_value)
        return env_value

    log.debug("Retrieving secret value %s from AWS Secrets manager", name)

    region = os.environ.get('AWS_REGION', None)
    if region is None:
        raise SecretsException(f"Could not get AWS_REGION environment variable value while resolving {name}")

    log.info("Fetching AWS Secret value for %s", name)
    arn_variable = f"{env_var_name}_ARN"
    arn = os.environ.get(arn_variable, None)
    if arn is None:
        raise SecretsException(f"Secret arn environment variable {arn_variable} not defined")

    return get_secret(arn, region, result_type)


def get_secret(secret_name: str,
               region: str,
               result_type=str,
               profile: str = None,
               endpoint_url: str = None):
    session = boto3.session.Session(profile_name=profile)
    client = session.client(
        service_name='secretsmanager',
        region_name=region,
        endpoint_url=endpoint_url
    )

    # In this sample we only handle
    # We rethrow the exception by default.

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    if 'SecretString' in get_secret_value_response:
        secret_value = get_secret_value_response['SecretString']
        if result_type == dict:
            return json.loads(secret_value)
        return secret_value

    return base64.b64decode(get_secret_value_response['SecretBinary'])
