from lambdas import init_lambda

init_lambda()


def handler(_event, _context):
    return {'status': 'OK'}
