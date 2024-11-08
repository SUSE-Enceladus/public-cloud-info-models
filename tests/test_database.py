import pytest

from pint_models.database import (
    create_db_logger,
    get_environ_entry,
    create_postgres_url_from_config,
)


def test_create_db_logger():
    create_db_logger('/tmp/test.txt')


def test_get_env_entry():
    with pytest.raises(Exception):
        get_environ_entry('pint_models_fake_entry')


def test_create_postgres_url_from_config():
    config = {
        'user': 'user1',
        'password': 'password',
        'dbname': 'db',
        'host': 'localhost',
        'port': 5432
    }
    url = create_postgres_url_from_config(config)
    assert url == 'postgresql://user1:password@localhost:5432/db'
