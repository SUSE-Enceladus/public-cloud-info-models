# Copyright (c) 2024 SUSE LLC
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import logging
import os
import re

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from pint_models.models import Base


def get_environ_entry(key_name):
    if key_name not in os.environ:
        raise Exception(f'Environment variable {key_name} is required.')
    return os.environ.get(key_name)


def create_db_logger(outputfile):
    """Function to setup logging of SQL statements

    Args:
        outputfile (filepath): The filepath where the SQL statements will be
            logged
    """
    if not outputfile:
        return

    db_log_file_name = outputfile
    db_handler_log_level = logging.INFO
    db_logger_log_level = logging.DEBUG

    db_handler = logging.FileHandler(db_log_file_name)
    db_handler.setLevel(db_handler_log_level)

    db_logger = logging.getLogger('sqlalchemy')
    db_logger.addHandler(db_handler)
    db_logger.setLevel(db_logger_log_level)


def create_postgres_url_from_config(dbconfig):
    """Create postgres connection string from provided config

    Args:
        dbconfig: (dict): A dictionary of config settings
            that are required to connect to the Postgres DB

    Returns:
        [string]: Postgres connection string
    """

    return _create_postgres_url(
        db_user=dbconfig.get('user'),
        db_password=dbconfig.get('password'),
        db_name=dbconfig.get('dbname'),
        db_host=dbconfig.get('host'),
        db_port=dbconfig.get('port'),
        # change the SSL stuff once we have a real DB to connect to
        db_ssl_mode='',
        db_root_cert=''
    )


def create_postgres_url_from_env():
    """Create postgres connection string from environment settings

    Returns:
        [string]: Postgres connection string
    """

    return _create_postgres_url(
        db_user=get_environ_entry('POSTGRES_USER'),
        db_password=get_environ_entry('POSTGRES_PASSWORD'),
        db_name=get_environ_entry('POSTGRES_DB'),
        db_host=get_environ_entry('POSTGRES_HOST'),
        db_port=os.environ.get('POSTGRES_PORT', 5432),
        db_ssl_mode=os.environ.get('POSTGRES_SSL_MODE', None),
        db_root_cert=os.environ.get('POSTGRES_SSL_ROOT_CERTIFICATE', None)
    )


def init_db(dbconfig=None, outputfile=None, echo=None,
            hide_parameters=None, create_all=False):
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    """Setup DB scoped session

    Args:
        config (dict): A dictionary of config settings
            that are required to connect to the Postgres DB
        outputfile (filepath): File location to log SQL statements
        echo (bool): Whether or not all statements are logged to the
            default log handler
            https://docs.sqlalchemy.org/en/14/core/engines.html#sqlalchemy.create_engine.params.echo
        hide_parameters (bool): if false then statement parameters
            will not be logged to INFO leverl log messages or in
            logged representation of error reports.
            https://docs.sqlalchemy.org/en/14/core/engines.html#sqlalchemy.create_engine.params.hide_parameters

    Returns:
        [scoped_session]: DB scoped_session to use for DB SQL operations
    """

    # Setup a dedicated DB logger if a target output file was provided
    create_db_logger(outputfile)

    # Create the DB engine, either from provided settings, or
    # using relevant environment settings.
    if dbconfig:
        engine_url = create_postgres_url_from_config(dbconfig)
    elif os.environ.get('DATABASE_URI', None):
        engine_url = os.environ['DATABASE_URI']
    else:
        engine_url = create_postgres_url_from_env()

    engine = create_engine(
        engine_url,
        echo=echo,
        hide_parameters=hide_parameters
    )

    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    Base.query = db_session.query_property()

    if create_all:
        Base.metadata.create_all(bind=engine)

    return db_session


def get_psql_server_version(db_session):
    """Return the psql server version"""
    result = db_session.execute(text("select version()"))
    for row in result:
        version = re.search(r'PostgreSQL\s+\d+.\d+', str(row))
        if version:
            break
    return version.group(0)


def _create_postgres_url(db_user, db_password, db_name, db_host,
                         db_port=5432, db_ssl_mode=None,
                         db_root_cert=None):
    """Helper function to construct the URL connection string

    Args:
        db_user: (string): the username to connect to the Postgres
            DB as
        db_password: (string): the password associated with the
            username being used to connect to the Postgres DB
        db_name: (string): the name of the Postgres DB to connect
            to
        db_host: (string): the host where the Postgres DB is
            running
        db_host: (number, optional): the port to connect to the
            Postgres DB at
        db_ssl_mode: (string, optional): the SSL mode to use when
            connecting to the Postgres DB
        db_root_cert: (string, optional): the root cert to use when
            connecting to the Postgres DB

    Returns:
        [string]: Postgres connection string
    """

    ssl_mode = ''
    if db_ssl_mode:
        # see
        # https://www.postgresql.org/docs/11/libpq-connect.html#
        # LIBPQ-CONNECT-SSLMODE
        ssl_mode = '?sslmode=%s' % (db_ssl_mode)
        if db_root_cert:
            ssl_mode += '&sslrootcert=%s' % (db_root_cert)

    return ('postgresql://%(user)s:%(password)s@%(host)s:%(port)s/'
            '%(db)s%(ssl)s' % {
                'user': db_user,
                'password': db_password,
                'db': db_name,
                'host': db_host,
                'port': db_port,
                'ssl': ssl_mode})
