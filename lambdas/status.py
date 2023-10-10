from lambdas import init_lambda
from lambdas.services.db_manager import with_db_session
from lambdas.services import status_service

init_lambda()


@with_db_session
def handler(_event, _context):
    return status_service.get_status()
