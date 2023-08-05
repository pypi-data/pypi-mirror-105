# testing/engines.py
# Copyright (C) 2005-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from __future__ import absolute_import

import collections
import re
import warnings
import weakref

from . import config
from .util import decorator
from .util import gc_collect
from .. import event
from .. import pool


class ConnectionKiller(object):
    def __init__(self):
        self.proxy_refs = weakref.WeakKeyDictionary()
        self.testing_engines = collections.defaultdict(set)
        self.dbapi_connections = set()

    def add_pool(self, pool):
        event.listen(pool, "checkout", self._add_conn)
        event.listen(pool, "checkin", self._remove_conn)
        event.listen(pool, "close", self._remove_conn)
        event.listen(pool, "close_detached", self._remove_conn)
        # note we are keeping "invalidated" here, as those are still
        # opened connections we would like to roll back

    def _add_conn(self, dbapi_con, con_record, con_proxy):
        self.dbapi_connections.add(dbapi_con)
        self.proxy_refs[con_proxy] = True

    def _remove_conn(self, dbapi_conn, *arg):
        self.dbapi_connections.discard(dbapi_conn)

    def add_engine(self, engine, scope):
        self.add_pool(engine.pool)

        assert scope in ("class", "global", "function", "fixture")
        self.testing_engines[scope].add(engine)

    def _safe(self, fn):
        try:
            fn()
        except Exception as e:
            warnings.warn(
                "testing_reaper couldn't rollback/close connection: %s" % e
            )

    def rollback_all(self):
        for rec in list(self.proxy_refs):
            if rec is not None and rec.is_valid:
                self._safe(rec.rollback)

    def checkin_all(self):
        # run pool.checkin() for all ConnectionFairy instances we have
        # tracked.

        for rec in list(self.proxy_refs):
            if rec is not None and rec.is_valid:
                self.dbapi_connections.discard(rec.connection)
                self._safe(rec._checkin)

        # for fairy refs that were GCed and could not close the connection,
        # such as asyncio, roll back those remaining connections
        for con in self.dbapi_connections:
            self._safe(con.rollback)
        self.dbapi_connections.clear()

    def close_all(self):
        self.checkin_all()

    def prepare_for_drop_tables(self, connection):
        # don't do aggressive checks for third party test suites
        if not config.bootstrapped_as_sqlalchemy:
            return

        from . import provision

        provision.prepare_for_drop_tables(connection.engine.url, connection)

    def _drop_testing_engines(self, scope):
        eng = self.testing_engines[scope]
        for rec in list(eng):
            for proxy_ref in list(self.proxy_refs):
                if proxy_ref is not None and proxy_ref.is_valid:
                    if (
                        proxy_ref._pool is not None
                        and proxy_ref._pool is rec.pool
                    ):
                        self._safe(proxy_ref._checkin)
            rec.dispose()
        eng.clear()

    def after_test(self):
        self._drop_testing_engines("function")

    def after_test_outside_fixtures(self, test):
        # don't do aggressive checks for third party test suites
        if not config.bootstrapped_as_sqlalchemy:
            return

        if test.__class__.__leave_connections_for_teardown__:
            return

        self.checkin_all()

        # on PostgreSQL, this will test for any "idle in transaction"
        # connections.   useful to identify tests with unusual patterns
        # that can't be cleaned up correctly.
        from . import provision

        with config.db.connect() as conn:
            provision.prepare_for_drop_tables(conn.engine.url, conn)

    def stop_test_class_inside_fixtures(self):
        self.checkin_all()
        self._drop_testing_engines("function")
        self._drop_testing_engines("class")

    def stop_test_class_outside_fixtures(self):
        # ensure no refs to checked out connections at all.

        if pool.base._strong_ref_connection_records:
            gc_collect()

            if pool.base._strong_ref_connection_records:
                ln = len(pool.base._strong_ref_connection_records)
                pool.base._strong_ref_connection_records.clear()
                assert (
                    False
                ), "%d connection recs not cleared after test suite" % (ln)

    def final_cleanup(self):
        self.checkin_all()
        for scope in self.testing_engines:
            self._drop_testing_engines(scope)

    def assert_all_closed(self):
        for rec in self.proxy_refs:
            if rec.is_valid:
                assert False


testing_reaper = ConnectionKiller()


@decorator
def assert_conns_closed(fn, *args, **kw):
    try:
        fn(*args, **kw)
    finally:
        testing_reaper.assert_all_closed()


@decorator
def rollback_open_connections(fn, *args, **kw):
    """Decorator that rolls back all open connections after fn execution."""

    try:
        fn(*args, **kw)
    finally:
        testing_reaper.rollback_all()


@decorator
def close_first(fn, *args, **kw):
    """Decorator that closes all connections before fn execution."""

    testing_reaper.checkin_all()
    fn(*args, **kw)


@decorator
def close_open_connections(fn, *args, **kw):
    """Decorator that closes all connections after fn execution."""
    try:
        fn(*args, **kw)
    finally:
        testing_reaper.checkin_all()


def all_dialects(exclude=None):
    import sqlalchemy.dialects as d

    for name in d.__all__:
        # TEMPORARY
        if exclude and name in exclude:
            continue
        mod = getattr(d, name, None)
        if not mod:
            mod = getattr(
                __import__("sqlalchemy.dialects.%s" % name).dialects, name
            )
        yield mod.dialect()


class ReconnectFixture(object):
    def __init__(self, dbapi):
        self.dbapi = dbapi
        self.connections = []
        self.is_stopped = False

    def __getattr__(self, key):
        return getattr(self.dbapi, key)

    def connect(self, *args, **kwargs):

        conn = self.dbapi.connect(*args, **kwargs)
        if self.is_stopped:
            self._safe(conn.close)
            curs = conn.cursor()  # should fail on Oracle etc.
            # should fail for everything that didn't fail
            # above, connection is closed
            curs.execute("select 1")
            assert False, "simulated connect failure didn't work"
        else:
            self.connections.append(conn)
            return conn

    def _safe(self, fn):
        try:
            fn()
        except Exception as e:
            warnings.warn("ReconnectFixture couldn't close connection: %s" % e)

    def shutdown(self, stop=False):
        # TODO: this doesn't cover all cases
        # as nicely as we'd like, namely MySQLdb.
        # would need to implement R. Brewer's
        # proxy server idea to get better
        # coverage.
        self.is_stopped = stop
        for c in list(self.connections):
            self._safe(c.close)
        self.connections = []

    def restart(self):
        self.is_stopped = False


def reconnecting_engine(url=None, options=None):
    url = url or config.db.url
    dbapi = config.db.dialect.dbapi
    if not options:
        options = {}
    options["module"] = ReconnectFixture(dbapi)
    engine = testing_engine(url, options)
    _dispose = engine.dispose

    def dispose():
        engine.dialect.dbapi.shutdown()
        engine.dialect.dbapi.is_stopped = False
        _dispose()

    engine.test_shutdown = engine.dialect.dbapi.shutdown
    engine.test_restart = engine.dialect.dbapi.restart
    engine.dispose = dispose
    return engine


def testing_engine(
    url=None,
    options=None,
    future=None,
    asyncio=False,
    transfer_staticpool=False,
):
    """Produce an engine configured by --options with optional overrides."""

    if asyncio:
        from sqlalchemy.ext.asyncio import create_async_engine as create_engine
    elif future or (
        config.db and config.db._is_future and future is not False
    ):
        from sqlalchemy.future import create_engine
    else:
        from sqlalchemy import create_engine
    from sqlalchemy.engine.url import make_url

    if not options:
        use_reaper = True
        scope = "function"
    else:
        use_reaper = options.pop("use_reaper", True)
        scope = options.pop("scope", "function")

    url = url or config.db.url

    url = make_url(url)
    if options is None:
        if config.db is None or url.drivername == config.db.url.drivername:
            options = config.db_opts
        else:
            options = {}
    elif config.db is not None and url.drivername == config.db.url.drivername:
        default_opt = config.db_opts.copy()
        default_opt.update(options)

    engine = create_engine(url, **options)

    if transfer_staticpool:
        from sqlalchemy.pool import StaticPool

        if config.db is not None and isinstance(config.db.pool, StaticPool):
            engine.pool._transfer_from(config.db.pool)

    if scope == "global":
        if asyncio:
            engine.sync_engine._has_events = True
        else:
            engine._has_events = (
                True  # enable event blocks, helps with profiling
            )

    if isinstance(engine.pool, pool.QueuePool):
        engine.pool._timeout = 0
        engine.pool._max_overflow = 0
    if use_reaper:
        testing_reaper.add_engine(engine, scope)

    return engine


def mock_engine(dialect_name=None):
    """Provides a mocking engine based on the current testing.db.

    This is normally used to test DDL generation flow as emitted
    by an Engine.

    It should not be used in other cases, as assert_compile() and
    assert_sql_execution() are much better choices with fewer
    moving parts.

    """

    from sqlalchemy import create_mock_engine

    if not dialect_name:
        dialect_name = config.db.name

    buffer = []

    def executor(sql, *a, **kw):
        buffer.append(sql)

    def assert_sql(stmts):
        recv = [re.sub(r"[\n\t]", "", str(s)) for s in buffer]
        assert recv == stmts, recv

    def print_sql():
        d = engine.dialect
        return "\n".join(str(s.compile(dialect=d)) for s in engine.mock)

    engine = create_mock_engine(dialect_name + "://", executor)
    assert not hasattr(engine, "mock")
    engine.mock = buffer
    engine.assert_sql = assert_sql
    engine.print_sql = print_sql
    return engine


class DBAPIProxyCursor(object):
    """Proxy a DBAPI cursor.

    Tests can provide subclasses of this to intercept
    DBAPI-level cursor operations.

    """

    def __init__(self, engine, conn, *args, **kwargs):
        self.engine = engine
        self.connection = conn
        self.cursor = conn.cursor(*args, **kwargs)

    def execute(self, stmt, parameters=None, **kw):
        if parameters:
            return self.cursor.execute(stmt, parameters, **kw)
        else:
            return self.cursor.execute(stmt, **kw)

    def executemany(self, stmt, params, **kw):
        return self.cursor.executemany(stmt, params, **kw)

    def __iter__(self):
        return iter(self.cursor)

    def __getattr__(self, key):
        return getattr(self.cursor, key)


class DBAPIProxyConnection(object):
    """Proxy a DBAPI connection.

    Tests can provide subclasses of this to intercept
    DBAPI-level connection operations.

    """

    def __init__(self, engine, cursor_cls):
        self.conn = engine.pool._creator()
        self.engine = engine
        self.cursor_cls = cursor_cls

    def cursor(self, *args, **kwargs):
        return self.cursor_cls(self.engine, self.conn, *args, **kwargs)

    def close(self):
        self.conn.close()

    def __getattr__(self, key):
        return getattr(self.conn, key)


def proxying_engine(
    conn_cls=DBAPIProxyConnection, cursor_cls=DBAPIProxyCursor
):
    """Produce an engine that provides proxy hooks for
    common methods.

    """

    def mock_conn():
        return conn_cls(config.db, cursor_cls)

    def _wrap_do_on_connect(do_on_connect):
        def go(dbapi_conn):
            return do_on_connect(dbapi_conn.conn)

        return go

    return testing_engine(
        options={
            "creator": mock_conn,
            "_wrap_do_on_connect": _wrap_do_on_connect,
        }
    )
