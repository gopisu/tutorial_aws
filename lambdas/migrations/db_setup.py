import json
import logging as log
import sys
from typing import Optional

from sqlalchemy import text

from lambdas import init_lambda
from lambdas.services import secrets_service
from lambdas.services.db_manager import DbManager

init_lambda()


def handler(event, _context):
    return setup_db(event)


def setup_db(event):
    action = event.get('action', None)
    if action is None:
        return {'success': False, 'message': "Action not defined"}

    if action not in ['create', 'drop-db', 'drop-user']:
        return {'success': False,
                'message': "Unknown action. Valid actions are 'create', 'drop-db' and 'drop-user'"}

    try:
        success: bool = False
        message: Optional[str] = None
        db_manager = DbManager(connection_secret='db-master-secret', db_name='postgres', isolation_level='AUTOCOMMIT')
        with db_manager as db:
            if action:
                if action == "create":
                    success, message = create_db(event, db)
                if action == "drop-db":
                    db_name = event.get('db_name')
                    if db_name is None:
                        secret = secrets_service.get_secret_value("db-app-secret", result_type=dict)
                        db_name = secret.get('dbname', 'exampledb')
                    success, message = drop_db(db_name, db)
                if action == "drop-user":
                    success, message = drop_user(event, db)
        db_manager.destroy()

        if action == "create":
            secret = secrets_service.get_secret_value("db-app-secret", result_type=dict)
            db_name = secret.get('dbname', 'exampledb')

            db_manager = DbManager(connection_secret='db-master-secret', db_name=db_name, isolation_level='AUTOCOMMIT')
            with db_manager as db:
                add_extensions(db)

        return {'success': success, 'message': message}

    except Exception:  # pylint: disable=broad-except
        message = f"setup database failed! Action {action}"
        log.exception(message)
        return {'success': False, 'message': message}


def create_db(event, db) -> tuple[bool, str]:
    log.info("Creating database role and schema based on db-app-secret")
    secret = secrets_service.get_secret_value("db-app-secret", result_type=dict)
    db_username = secret['username']
    password = secret['password']
    db_name = secret.get('dbname', 'exampledb')

    if not postgres_user_exists(user_name=db_username, db=db):
        add_postgres_user(username=db_username, password=password, db=db)

    if not database_exists(db_name, db):
        encoding = event.get('encoding', 'en_US.UTF8')
        create_data_base(db_name=db_name, owner=db_username, encoding=encoding, db=db)
        return True, f"Database role and schema created. dbname: {db_name} user: {db_username} pwd: {password}"

    return False, 'Database already exists'


def add_extensions(db):
    log.info("Creating extensions")
    db.session.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
    db.session.commit()
    log.info("Extensions created")
    return True


def drop_db(db_name: str, db) -> tuple[bool, str]:
    log.info("Dropping database schema")
    if "'" in db_name:
        raise Exception("Bad database name")  # pylint:disable=broad-exception-raised

    db.session.execute(text("""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = :database_name
        AND pid <> pg_backend_pid()"""), {'database_name': db_name})

    db.session.execute(text(f"DROP DATABASE {db_name}"))
    db.session.commit()
    return True, 'Database schema dropped'


def drop_user(event, db) -> tuple[bool, str]:
    log.info("Dropping database user")

    username = event['username']
    if "'" in username:
        raise Exception("Bad database user name")  # pylint:disable=broad-exception-raised

    db.session.execute(text(f"DROP USER {username}"))
    db.session.commit()
    return True, 'Database user dropped'


def postgres_user_exists(user_name, db):
    result = db.session.execute(text('select rolname from pg_catalog.pg_roles where rolname = :user_name'),
                                {'user_name': user_name}).one_or_none()

    return result is not None


def database_exists(db_name, db):
    result = db.session.execute(text("SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = :db_name"),
                                {'db_name': db_name.lower()}).one_or_none()

    return result is not None


def add_postgres_user(username, password, db):
    if "'" in username:
        raise Exception("Bad username")  # pylint:disable=broad-exception-raised
    db.session.execute(text("CREATE ROLE " + username + " LOGIN PASSWORD :password"),
                       {'password': password})
    db.session.commit()


def create_data_base(db_name: str, owner: str, encoding: str, db):
    if "'" in db_name:
        raise Exception("Bad database name")  # pylint:disable=broad-exception-raised

    if "'" in owner:
        raise Exception("Bad migrations owner")  # pylint:disable=broad-exception-raised

    db.session.execute(text(f"GRANT {owner} to {db.username}"))
    db.session.commit()

    db.session.execute(text(f"CREATE DATABASE {db_name} "
                            f"WITH OWNER={owner} "
                            f"TEMPLATE=template0 "
                            f"ENCODING=:encoding "
                            f"LC_COLLATE=:collate "
                            f"LC_CTYPE=:ctype"),
                       {'encoding': 'UTF8',
                        'collate': encoding,
                        'ctype': encoding
                        })
    db.session.commit()


if __name__ == "__main__":
    payload = json.loads(sys.argv[1])
    response = handler(event=payload, _context=None)
    log.info(response)
