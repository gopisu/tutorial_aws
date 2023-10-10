from lambdas.models import ExampleData
from lambdas.services.db_manager import get_app_db

db = get_app_db()


def find_data() -> list[ExampleData]:
    return db.session.query(ExampleData).all()
