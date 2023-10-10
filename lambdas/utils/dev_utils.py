import json
import os

ENVIRONMENT = os.environ.get('ENVIRONMENT', 'DEV').upper()


def is_dev():
    return ENVIRONMENT == 'DEV' or is_local()


def is_local():
    return ENVIRONMENT == 'LOCAL'


def get_mock_data(path: str) -> dict:
    with open(file=path, mode='r', encoding='utf8') as file:
        return json.load(file)
