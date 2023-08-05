from .. import util
from ..engine import Connection as _LegacyConnection
from ..engine import create_engine as _create_engine
from ..engine import Engine as _LegacyEngine
from ..engine.base import OptionEngineMixin

NO_OPTIONS = util.immutabledict()


def create_engine(*arg, **kw):
    """Create a new :class:`_future.Engine` instance.

    Arguments passed to :func:`_future.create_engine` are mostly identical
    to those passed to the 1.x :func:`_sa.create_engine` function.
    The difference is that the object returned is the :class:`._future.Engine`
    which has the 2.0 version of the API.

    """

    kw["_future_engine_class"] = Engine
    return _create_engine(*arg, **kw)


class Connection(_LegacyConnection):
    """Provides high-level functionality for a wrapped DB-API connection.

    The :class:`_future.Connection` object is procured by calling
    the :meth:`_future.Engine.connect` method of the :class:`_future.Engine`
    object, and provides services for execution of SQL statements as well
    as transaction control.

    **This is the SQLAlchemy 2.0 version** of the :class:`_engine.Connection`
    class.   The API and behavior of this object is largely the same, with the
    following differences in behavior:

    * The result object returned for results is the
      :class:`_engine.CursorResult`
      object, which is a subclass of the :class:`_engine.Result`.
      This object has a slightly different API and behavior than the
      :class:`_engine.LegacyCursorResult` returned for 1.x style usage.

    * The object has :meth:`_future.Connection.commit` and
      :meth:`_future.Connection.rollback` methods which commit or roll back
      the current transaction in progress, if any.

    * The object features "autobegin" behavior, such that any call to
      :meth:`_future.Connection.execute` will
      unconditionally start a
      transaction which can be controlled using the above mentioned
      :meth:`_future.Connection.commit` and
      :meth:`_future.Connection.rollback` methods.

    * The object does not have any "autocommit" functionality.  Any SQL
      statement or DDL statement will not be followed by any COMMIT until
      the transaction is explicitly committed, either via the
      :meth:`_future.Connection.commit` method, or if the connection is
      being used in a context manager that commits such as the one
      returned by :meth:`_future.Engine.begin`.

    * The SAVEPOINT method :meth:`_future.Connection.begin_nested` returns
      a :class:`_engine.NestedTransaction` as was always the case, and the
      savepoint can be controlled by invoking
      :meth:`_engine.NestedTransaction.commit` or
      :meth:`_engine.NestedTransaction.rollback` as was the case before.
      However, this savepoint "transaction" is not associated with the
      transaction that is controlled by the connection itself; the overall
      transaction can be committed or rolled back directly which will not emit
      any special instructions for the SAVEPOINT (this will typically have the
      effect that one desires).

    * The :class:`_future.Connection` object does not support "branching",
      which was a pattern by which a sub "connection" would be used that
      refers to this connection as a parent.



    """

    _is_future = True

    def _branch(self):
        raise NotImplementedError(
            "sqlalchemy.future.Connection does not support "
            "'branching' of new connections."
        )

    def begin(self):
        """Begin a transaction prior to autobegin occurring.

        The returned object is an instance of :class:`_engine.RootTransaction`.
        This object represents the "scope" of the transaction,
        which completes when either the :meth:`_engine.Transaction.rollback`
        or :meth:`_engine.Transaction.commit` method is called.

        The :meth:`_future.Connection.begin` method in SQLAlchemy 2.0 begins a
        transaction that normally will be begun in any case when the connection
        is first used to execute a statement.  The reason this method might be
        used would be to invoke the :meth:`_events.ConnectionEvents.begin`
        event at a specific time, or to organize code within the scope of a
        connection checkout in terms of context managed blocks, such as::

            with engine.connect() as conn:
                with conn.begin():
                    conn.execute(...)
                    conn.execute(...)

                with conn.begin():
                    conn.execute(...)
                    conn.execute(...)

        The above code is not  fundamentally any different in its behavior than
        the following code  which does not use
        :meth:`_future.Connection.begin`; the below style is referred towards
        as "commit as you go" style::

            with engine.connect() as conn:
                conn.execute(...)
                conn.execute(...)
                conn.commit()

                conn.execute(...)
                conn.execute(...)
                conn.commit()

        From a database point of view, the :meth:`_future.Connection.begin`
        method does not emit any SQL or change the state of the underlying
        DBAPI connection in any way; the Python DBAPI does not have any
        concept of explicit transaction begin.

        .. seealso::

            :ref:`tutorial_working_with_transactions` - in the
            :ref:`unified_tutorial`

            :meth:`_future.Connection.begin_nested` - use a SAVEPOINT

            :meth:`_engine.Connection.begin_twophase` -
            use a two phase /XID transaction

            :meth:`_future.Engine.begin` - context manager available from
            :class:`_future.Engine`

        """
        return super(Connection, self).begin()

    def begin_nested(self):
        """Begin a nested transaction (i.e. SAVEPOINT) and return a transaction
        handle.

        The returned object is an instance of
        :class:`_engine.NestedTransaction`.

        Nested transactions require SAVEPOINT support in the
        underlying database.  Any transaction in the hierarchy may
        ``commit`` and ``rollback``, however the outermost transaction
        still controls the overall ``commit`` or ``rollback`` of the
        transaction of a whole.

        If an outer :class:`.RootTransaction` is not present on this
        :class:`_future.Connection`, a new one is created using "autobegin".
        This outer transaction may be completed using "commit-as-you-go" style
        usage, by calling upon :meth:`_future.Connection.commit` or
        :meth:`_future.Connection.rollback`.

        .. tip::

            The "autobegin" behavior of :meth:`_future.Connection.begin_nested`
            is specific to :term:`2.0 style` use; for legacy behaviors, see
            :meth:`_engine.Connection.begin_nested`.

        The :class:`_engine.NestedTransaction` remains independent of the
        :class:`_future.Connection` object itself. Calling the
        :meth:`_future.Connection.commit` or
        :meth:`_future.Connection.rollback` will always affect the actual
        containing database transaction itself, and not the SAVEPOINT itself.
        When a database transaction is committed, any SAVEPOINTs that have been
        established are cleared and the data changes within their scope is also
        committed.

        .. seealso::

            :meth:`_future.Connection.begin`


        """
        return super(Connection, self).begin_nested()

    def commit(self):
        """Commit the transaction that is currently in progress.

        This method commits the current transaction if one has been started.
        If no transaction was started, the method has no effect, assuming
        the connection is in a non-invalidated state.

        A transaction is begun on a :class:`_future.Connection` automatically
        whenever a statement is first executed, or when the
        :meth:`_future.Connection.begin` method is called.

        .. note:: The :meth:`_future.Connection.commit` method only acts upon
          the primary database transaction that is linked to the
          :class:`_future.Connection` object.  It does not operate upon a
          SAVEPOINT that would have been invoked from the
          :meth:`_future.Connection.begin_nested` method; for control of a
          SAVEPOINT, call :meth:`_engine.NestedTransaction.commit` on the
          :class:`_engine.NestedTransaction` that is returned by the
          :meth:`_future.Connection.begin_nested` method itself.


        """
        if self._transaction:
            self._transaction.commit()

    def rollback(self):
        """Roll back the transaction that is currently in progress.

        This method rolls back the current transaction if one has been started.
        If no transaction was started, the method has no effect.  If a
        transaction was started and the connection is in an invalidated state,
        the transaction is cleared using this method.

        A transaction is begun on a :class:`_future.Connection` automatically
        whenever a statement is first executed, or when the
        :meth:`_future.Connection.begin` method is called.

        .. note:: The :meth:`_future.Connection.rollback` method only acts
          upon the primary database transaction that is linked to the
          :class:`_future.Connection` object.  It does not operate upon a
          SAVEPOINT that would have been invoked from the
          :meth:`_future.Connection.begin_nested` method; for control of a
          SAVEPOINT, call :meth:`_engine.NestedTransaction.rollback` on the
          :class:`_engine.NestedTransaction` that is returned by the
          :meth:`_future.Connection.begin_nested` method itself.


        """
        if self._transaction:
            self._transaction.rollback()

    def close(self):
        """Close this :class:`_future.Connection`.

        This has the effect of also calling :meth:`_future.Connection.rollback`
        if any transaction is in place.

        """
        super(Connection, self).close()

    def execute(self, statement, parameters=None, execution_options=None):
        r"""Executes a SQL statement construct and returns a
        :class:`_engine.Result`.

        :param statement: The statement to be executed.  This is always
         an object that is in both the :class:`_expression.ClauseElement` and
         :class:`_expression.Executable` hierarchies, including:

         * :class:`_expression.Select`
         * :class:`_expression.Insert`, :class:`_expression.Update`,
           :class:`_expression.Delete`
         * :class:`_expression.TextClause` and
           :class:`_expression.TextualSelect`
         * :class:`_schema.DDL` and objects which inherit from
           :class:`_schema.DDLElement`

        :param parameters: parameters which will be bound into the statement.
         This may be either a dictionary of parameter names to values,
         or a mutable sequence (e.g. a list) of dictionaries.  When a
         list of dictionaries is passed, the underlying statement execution
         will make use of the DBAPI ``cursor.executemany()`` method.
         When a single dictionary is passed, the DBAPI ``cursor.execute()``
         method will be used.

        :param execution_options: optional dictionary of execution options,
         which will be associated with the statement execution.  This
         dictionary can provide a subset of the options that are accepted
         by :meth:`_future.Connection.execution_options`.

        :return: a :class:`_engine.Result` object.

        """
        return self._execute_20(
            statement, parameters, execution_options or NO_OPTIONS
        )

    def scalar(self, statement, parameters=None, execution_options=None):
        r"""Executes a SQL statement construct and returns a scalar object.

        This method is shorthand for invoking the
        :meth:`_engine.Result.scalar` method after invoking the
        :meth:`_future.Connection.execute` method.  Parameters are equivalent.

        :return: a scalar Python value representing the first column of the
         first row returned.

        """
        return self.execute(statement, parameters, execution_options).scalar()


class Engine(_LegacyEngine):
    """Connects a :class:`_pool.Pool` and
    :class:`_engine.Dialect` together to provide a
    source of database connectivity and behavior.

    **This is the SQLAlchemy 2.0 version** of the :class:`~.engine.Engine`.

    An :class:`.future.Engine` object is instantiated publicly using the
    :func:`~sqlalchemy.future.create_engine` function.

    .. seealso::

        :doc:`/core/engines`

        :ref:`connections_toplevel`

    """

    _connection_cls = Connection
    _is_future = True

    def _not_implemented(self, *arg, **kw):
        raise NotImplementedError(
            "This method is not implemented for SQLAlchemy 2.0."
        )

    transaction = (
        run_callable
    ) = (
        execute
    ) = (
        scalar
    ) = (
        _execute_clauseelement
    ) = _execute_compiled = table_names = has_table = _not_implemented

    def _run_ddl_visitor(self, visitorcallable, element, **kwargs):
        # TODO: this is for create_all support etc.   not clear if we
        # want to provide this in 2.0, that is, a way to execute SQL where
        # they aren't calling "engine.begin()" explicitly, however, DDL
        # may be a special case for which we want to continue doing it this
        # way.  A big win here is that the full DDL sequence is inside of a
        # single transaction rather than COMMIT for each statement.
        with self.begin() as conn:
            conn._run_ddl_visitor(visitorcallable, element, **kwargs)

    @classmethod
    def _future_facade(self, legacy_engine):
        return Engine(
            legacy_engine.pool,
            legacy_engine.dialect,
            legacy_engine.url,
            logging_name=legacy_engine.logging_name,
            echo=legacy_engine.echo,
            hide_parameters=legacy_engine.hide_parameters,
            execution_options=legacy_engine._execution_options,
        )

    class _trans_ctx(object):
        def __init__(self, conn):
            self.conn = conn

        def __enter__(self):
            self.transaction = self.conn.begin()
            self.transaction.__enter__()
            return self.conn

        def __exit__(self, type_, value, traceback):
            try:
                self.transaction.__exit__(type_, value, traceback)
            finally:
                self.conn.close()

    def begin(self):
        """Return a :class:`_future.Connection` object with a transaction
        begun.

        Use of this method is similar to that of
        :meth:`_future.Engine.connect`, typically as a context manager, which
        will automatically maintain the state of the transaction when the block
        ends, either by calling :meth:`_future.Connection.commit` when the
        block succeeds normally, or :meth:`_future.Connection.rollback` when an
        exception is raised, before propagating the exception outwards::

            with engine.begin() as connection:
                connection.execute(text("insert into table values ('foo')"))


        .. seealso::

            :meth:`_future.Engine.connect`

            :meth:`_future.Connection.begin`

        """
        conn = self.connect()
        return self._trans_ctx(conn)

    def connect(self):
        """Return a new :class:`_future.Connection` object.

        The :class:`_future.Connection` acts as a Python context manager, so
        the typical use of this method looks like::

            with engine.connect() as connection:
                connection.execute(text("insert into table values ('foo')"))
                connection.commit()

        Where above, after the block is completed, the connection is "closed"
        and its underlying DBAPI resources are returned to the connection pool.
        This also has the effect of rolling back any transaction that
        was explicitly begun or was begun via autobegin, and will
        emit the :meth:`_events.ConnectionEvents.rollback` event if one was
        started and is still in progress.

        .. seealso::

            :meth:`_future.Engine.begin`


        """
        return super(Engine, self).connect()


class OptionEngine(OptionEngineMixin, Engine):
    pass


Engine._option_cls = OptionEngine
