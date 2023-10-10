from dao import example_dao
from lambdas.services.db_manager import get_app_db

db = get_app_db()


def get_status() -> dict:
    data = example_dao.find_data()
    return {'status': 'OK', 'dataSize': len(data)}
