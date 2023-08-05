# mysql/pyodbc.py
# Copyright (C) 2005-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

r"""


.. dialect:: mysql+pyodbc
    :name: PyODBC
    :dbapi: pyodbc
    :connectstring: mysql+pyodbc://<username>:<password>@<dsnname>
    :url: http://pypi.python.org/pypi/pyodbc/

.. note::

    The PyODBC for MySQL dialect is **not tested as part of
    SQLAlchemy's continuous integration**.
    The recommended MySQL dialects are mysqlclient and PyMySQL.
    However, if you want to use the mysql+pyodbc dialect and require
    full support for ``utf8mb4`` characters (including supplementary
    characters like emoji) be sure to use a current release of
    MySQL Connector/ODBC and specify the "ANSI" (**not** "Unicode")
    version of the driver in your DSN or connection string.

Pass through exact pyodbc connection string::

    import urllib
    connection_string = (
        'DRIVER=MySQL ODBC 8.0 ANSI Driver;'
        'SERVER=localhost;'
        'PORT=3307;'
        'DATABASE=mydb;'
        'UID=root;'
        'PWD=(whatever);'
        'charset=utf8mb4;'
    )
    params = urllib.parse.quote_plus(connection_string)
    connection_uri = "mysql+pyodbc:///?odbc_connect=%s" % params

"""  # noqa

import re
import sys

from .base import MySQLDialect
from .base import MySQLExecutionContext
from .types import TIME
from ... import util
from ...connectors.pyodbc import PyODBCConnector
from ...sql.sqltypes import Time


class _pyodbcTIME(TIME):
    def result_processor(self, dialect, coltype):
        def process(value):
            # pyodbc returns a datetime.time object; no need to convert
            return value

        return process


class MySQLExecutionContext_pyodbc(MySQLExecutionContext):
    def get_lastrowid(self):
        cursor = self.create_cursor()
        cursor.execute("SELECT LAST_INSERT_ID()")
        lastrowid = cursor.fetchone()[0]
        cursor.close()
        return lastrowid


class MySQLDialect_pyodbc(PyODBCConnector, MySQLDialect):
    supports_statement_cache = True
    colspecs = util.update_copy(MySQLDialect.colspecs, {Time: _pyodbcTIME})
    supports_unicode_statements = True
    execution_ctx_cls = MySQLExecutionContext_pyodbc

    pyodbc_driver_name = "MySQL"

    def _detect_charset(self, connection):
        """Sniff out the character set in use for connection results."""

        # Prefer 'character_set_results' for the current connection over the
        # value in the driver.  SET NAMES or individual variable SETs will
        # change the charset without updating the driver's view of the world.
        #
        # If it's decided that issuing that sort of SQL leaves you SOL, then
        # this can prefer the driver value.
        rs = connection.exec_driver_sql(
            "SHOW VARIABLES LIKE 'character_set%%'"
        )
        opts = {row[0]: row[1] for row in self._compat_fetchall(rs)}
        for key in ("character_set_connection", "character_set"):
            if opts.get(key, None):
                return opts[key]

        util.warn(
            "Could not detect the connection character set.  "
            "Assuming latin1."
        )
        return "latin1"

    def _extract_error_code(self, exception):
        m = re.compile(r"\((\d+)\)").search(str(exception.args))
        c = m.group(1)
        if c:
            return int(c)
        else:
            return None

    def on_connect(self):
        super_ = super(MySQLDialect_pyodbc, self).on_connect()

        def on_connect(conn):
            if super_ is not None:
                super_(conn)

            # declare Unicode encoding for pyodbc as per
            #   https://github.com/mkleehammer/pyodbc/wiki/Unicode
            pyodbc_SQL_CHAR = 1  # pyodbc.SQL_CHAR
            pyodbc_SQL_WCHAR = -8  # pyodbc.SQL_WCHAR
            if sys.version_info.major > 2:
                conn.setdecoding(pyodbc_SQL_CHAR, encoding="utf-8")
                conn.setdecoding(pyodbc_SQL_WCHAR, encoding="utf-8")
                conn.setencoding(encoding="utf-8")
            else:
                conn.setdecoding(pyodbc_SQL_CHAR, encoding="utf-8")
                conn.setdecoding(pyodbc_SQL_WCHAR, encoding="utf-8")
                conn.setencoding(str, encoding="utf-8")
                conn.setencoding(unicode, encoding="utf-8")  # noqa: F821

        return on_connect


dialect = MySQLDialect_pyodbc
