# sqlalchemy/exc.py
# Copyright (C) 2005-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""Exceptions used with SQLAlchemy.

The base exception class is :exc:`.SQLAlchemyError`.  Exceptions which are
raised as a result of DBAPI exceptions are all subclasses of
:exc:`.DBAPIError`.

"""

from .util import _preloaded
from .util import compat

_version_token = None


class SQLAlchemyError(Exception):
    """Generic error class."""

    code = None

    def __init__(self, *arg, **kw):
        code = kw.pop("code", None)
        if code is not None:
            self.code = code
        super(SQLAlchemyError, self).__init__(*arg, **kw)

    def _code_str(self):
        if not self.code:
            return ""
        else:
            return (
                "(Background on this error at: "
                "http://sqlalche.me/e/%s/%s)"
                % (
                    _version_token,
                    self.code,
                )
            )

    def _message(self, as_unicode=compat.py3k):
        # rules:
        #
        # 1. under py2k, for __str__ return single string arg as it was
        # given without converting to unicode.  for __unicode__
        # do a conversion but check that it's not unicode already just in
        # case
        #
        # 2. under py3k, single arg string will usually be a unicode
        # object, but since __str__() must return unicode, check for
        # bytestring just in case
        #
        # 3. for multiple self.args, this is not a case in current
        # SQLAlchemy though this is happening in at least one known external
        # library, call str() which does a repr().
        #
        if len(self.args) == 1:
            text = self.args[0]

            if as_unicode and isinstance(text, compat.binary_types):
                text = compat.decode_backslashreplace(text, "utf-8")
            # This is for when the argument is not a string of any sort.
            # Otherwise, converting this exception to string would fail for
            # non-string arguments.
            elif compat.py3k or not as_unicode:
                text = str(text)
            else:
                text = compat.text_type(text)

            return text
        else:
            # this is not a normal case within SQLAlchemy but is here for
            # compatibility with Exception.args - the str() comes out as
            # a repr() of the tuple
            return str(self.args)

    def _sql_message(self, as_unicode):
        message = self._message(as_unicode)

        if self.code:
            message = "%s %s" % (message, self._code_str())

        return message

    def __str__(self):
        return self._sql_message(compat.py3k)

    def __unicode__(self):
        return self._sql_message(as_unicode=True)


class ArgumentError(SQLAlchemyError):
    """Raised when an invalid or conflicting function argument is supplied.

    This error generally corresponds to construction time state errors.

    """


class ObjectNotExecutableError(ArgumentError):
    """Raised when an object is passed to .execute() that can't be
    executed as SQL.

    .. versionadded:: 1.1

    """

    def __init__(self, target):
        super(ObjectNotExecutableError, self).__init__(
            "Not an executable object: %r" % target
        )


class NoSuchModuleError(ArgumentError):
    """Raised when a dynamically-loaded module (usually a database dialect)
    of a particular name cannot be located."""


class NoForeignKeysError(ArgumentError):
    """Raised when no foreign keys can be located between two selectables
    during a join."""


class AmbiguousForeignKeysError(ArgumentError):
    """Raised when more than one foreign key matching can be located
    between two selectables during a join."""


class CircularDependencyError(SQLAlchemyError):
    """Raised by topological sorts when a circular dependency is detected.

    There are two scenarios where this error occurs:

    * In a Session flush operation, if two objects are mutually dependent
      on each other, they can not be inserted or deleted via INSERT or
      DELETE statements alone; an UPDATE will be needed to post-associate
      or pre-deassociate one of the foreign key constrained values.
      The ``post_update`` flag described at :ref:`post_update` can resolve
      this cycle.
    * In a :attr:`_schema.MetaData.sorted_tables` operation, two
      :class:`_schema.ForeignKey`
      or :class:`_schema.ForeignKeyConstraint` objects mutually refer to each
      other.  Apply the ``use_alter=True`` flag to one or both,
      see :ref:`use_alter`.

    """

    def __init__(self, message, cycles, edges, msg=None, code=None):
        if msg is None:
            message += " (%s)" % ", ".join(repr(s) for s in cycles)
        else:
            message = msg
        SQLAlchemyError.__init__(self, message, code=code)
        self.cycles = cycles
        self.edges = edges

    def __reduce__(self):
        return self.__class__, (None, self.cycles, self.edges, self.args[0])


class CompileError(SQLAlchemyError):
    """Raised when an error occurs during SQL compilation"""


class UnsupportedCompilationError(CompileError):
    """Raised when an operation is not supported by the given compiler.

    .. seealso::

        :ref:`faq_sql_expression_string`

        :ref:`error_l7de`
    """

    code = "l7de"

    def __init__(self, compiler, element_type, message=None):
        super(UnsupportedCompilationError, self).__init__(
            "Compiler %r can't render element of type %s%s"
            % (compiler, element_type, ": %s" % message if message else "")
        )


class IdentifierError(SQLAlchemyError):
    """Raised when a schema name is beyond the max character limit"""


class DisconnectionError(SQLAlchemyError):
    """A disconnect is detected on a raw DB-API connection.

    This error is raised and consumed internally by a connection pool.  It can
    be raised by the :meth:`_events.PoolEvents.checkout`
    event so that the host pool
    forces a retry; the exception will be caught three times in a row before
    the pool gives up and raises :class:`~sqlalchemy.exc.InvalidRequestError`
    regarding the connection attempt.

    """

    invalidate_pool = False


class InvalidatePoolError(DisconnectionError):
    """Raised when the connection pool should invalidate all stale connections.

    A subclass of :class:`_exc.DisconnectionError` that indicates that the
    disconnect situation encountered on the connection probably means the
    entire pool should be invalidated, as the database has been restarted.

    This exception will be handled otherwise the same way as
    :class:`_exc.DisconnectionError`, allowing three attempts to reconnect
    before giving up.

    .. versionadded:: 1.2

    """

    invalidate_pool = True


class TimeoutError(SQLAlchemyError):  # noqa
    """Raised when a connection pool times out on getting a connection."""


class InvalidRequestError(SQLAlchemyError):
    """SQLAlchemy was asked to do something it can't do.

    This error generally corresponds to runtime state errors.

    """


class NoInspectionAvailable(InvalidRequestError):
    """A subject passed to :func:`sqlalchemy.inspection.inspect` produced
    no context for inspection."""


class PendingRollbackError(InvalidRequestError):
    """A transaction has failed and needs to be rolled back before
    continuing.

    .. versionadded:: 1.4

    """


class ResourceClosedError(InvalidRequestError):
    """An operation was requested from a connection, cursor, or other
    object that's in a closed state."""


class NoSuchColumnError(KeyError, InvalidRequestError):
    """A nonexistent column is requested from a ``Row``."""


class NoResultFound(InvalidRequestError):
    """A database result was required but none was found.


    .. versionchanged:: 1.4  This exception is now part of the
       ``sqlalchemy.exc`` module in Core, moved from the ORM.  The symbol
       remains importable from ``sqlalchemy.orm.exc``.


    """


class MultipleResultsFound(InvalidRequestError):
    """A single database result was required but more than one were found.

    .. versionchanged:: 1.4  This exception is now part of the
       ``sqlalchemy.exc`` module in Core, moved from the ORM.  The symbol
       remains importable from ``sqlalchemy.orm.exc``.


    """


class NoReferenceError(InvalidRequestError):
    """Raised by ``ForeignKey`` to indicate a reference cannot be resolved."""


class AwaitRequired(InvalidRequestError):
    """Error raised by the async greenlet spawn if no async operation
    was awaited when it required one.

    """

    code = "xd1r"


class MissingGreenlet(InvalidRequestError):
    r"""Error raised by the async greenlet await\_ if called while not inside
    the greenlet spawn context.

    """

    code = "xd2s"


class NoReferencedTableError(NoReferenceError):
    """Raised by ``ForeignKey`` when the referred ``Table`` cannot be
    located.

    """

    def __init__(self, message, tname):
        NoReferenceError.__init__(self, message)
        self.table_name = tname

    def __reduce__(self):
        return self.__class__, (self.args[0], self.table_name)


class NoReferencedColumnError(NoReferenceError):
    """Raised by ``ForeignKey`` when the referred ``Column`` cannot be
    located.

    """

    def __init__(self, message, tname, cname):
        NoReferenceError.__init__(self, message)
        self.table_name = tname
        self.column_name = cname

    def __reduce__(self):
        return (
            self.__class__,
            (self.args[0], self.table_name, self.column_name),
        )


class NoSuchTableError(InvalidRequestError):
    """Table does not exist or is not visible to a connection."""


class UnreflectableTableError(InvalidRequestError):
    """Table exists but can't be reflected for some reason.

    .. versionadded:: 1.2

    """


class UnboundExecutionError(InvalidRequestError):
    """SQL was attempted without a database connection to execute it on."""


class DontWrapMixin(object):
    """A mixin class which, when applied to a user-defined Exception class,
    will not be wrapped inside of :exc:`.StatementError` if the error is
    emitted within the process of executing a statement.

    E.g.::

        from sqlalchemy.exc import DontWrapMixin

        class MyCustomException(Exception, DontWrapMixin):
            pass

        class MySpecialType(TypeDecorator):
            impl = String

            def process_bind_param(self, value, dialect):
                if value == 'invalid':
                    raise MyCustomException("invalid!")

    """


class StatementError(SQLAlchemyError):
    """An error occurred during execution of a SQL statement.

    :class:`StatementError` wraps the exception raised
    during execution, and features :attr:`.statement`
    and :attr:`.params` attributes which supply context regarding
    the specifics of the statement which had an issue.

    The wrapped exception object is available in
    the :attr:`.orig` attribute.

    """

    statement = None
    """The string SQL statement being invoked when this exception occurred."""

    params = None
    """The parameter list being used when this exception occurred."""

    orig = None
    """The DBAPI exception object."""

    ismulti = None

    def __init__(
        self,
        message,
        statement,
        params,
        orig,
        hide_parameters=False,
        code=None,
        ismulti=None,
    ):
        SQLAlchemyError.__init__(self, message, code=code)
        self.statement = statement
        self.params = params
        self.orig = orig
        self.ismulti = ismulti
        self.hide_parameters = hide_parameters
        self.detail = []

    def add_detail(self, msg):
        self.detail.append(msg)

    def __reduce__(self):
        return (
            self.__class__,
            (
                self.args[0],
                self.statement,
                self.params,
                self.orig,
                self.hide_parameters,
                self.ismulti,
            ),
        )

    @_preloaded.preload_module("sqlalchemy.sql.util")
    def _sql_message(self, as_unicode):
        util = _preloaded.preloaded.sql_util

        details = [self._message(as_unicode=as_unicode)]
        if self.statement:
            if not as_unicode and not compat.py3k:
                stmt_detail = "[SQL: %s]" % compat.safe_bytestring(
                    self.statement
                )
            else:
                stmt_detail = "[SQL: %s]" % self.statement
            details.append(stmt_detail)
            if self.params:
                if self.hide_parameters:
                    details.append(
                        "[SQL parameters hidden due to hide_parameters=True]"
                    )
                else:
                    params_repr = util._repr_params(
                        self.params, 10, ismulti=self.ismulti
                    )
                    details.append("[parameters: %r]" % params_repr)
        code_str = self._code_str()
        if code_str:
            details.append(code_str)
        return "\n".join(["(%s)" % det for det in self.detail] + details)


class DBAPIError(StatementError):
    """Raised when the execution of a database operation fails.

    Wraps exceptions raised by the DB-API underlying the
    database operation.  Driver-specific implementations of the standard
    DB-API exception types are wrapped by matching sub-types of SQLAlchemy's
    :class:`DBAPIError` when possible.  DB-API's ``Error`` type maps to
    :class:`DBAPIError` in SQLAlchemy, otherwise the names are identical.  Note
    that there is no guarantee that different DB-API implementations will
    raise the same exception type for any given error condition.

    :class:`DBAPIError` features :attr:`~.StatementError.statement`
    and :attr:`~.StatementError.params` attributes which supply context
    regarding the specifics of the statement which had an issue, for the
    typical case when the error was raised within the context of
    emitting a SQL statement.

    The wrapped exception object is available in the
    :attr:`~.StatementError.orig` attribute. Its type and properties are
    DB-API implementation specific.

    """

    code = "dbapi"

    @classmethod
    def instance(
        cls,
        statement,
        params,
        orig,
        dbapi_base_err,
        hide_parameters=False,
        connection_invalidated=False,
        dialect=None,
        ismulti=None,
    ):
        # Don't ever wrap these, just return them directly as if
        # DBAPIError didn't exist.
        if (
            isinstance(orig, BaseException) and not isinstance(orig, Exception)
        ) or isinstance(orig, DontWrapMixin):
            return orig

        if orig is not None:
            # not a DBAPI error, statement is present.
            # raise a StatementError
            if isinstance(orig, SQLAlchemyError) and statement:
                return StatementError(
                    "(%s.%s) %s"
                    % (
                        orig.__class__.__module__,
                        orig.__class__.__name__,
                        orig.args[0],
                    ),
                    statement,
                    params,
                    orig,
                    hide_parameters=hide_parameters,
                    code=orig.code,
                    ismulti=ismulti,
                )
            elif not isinstance(orig, dbapi_base_err) and statement:
                return StatementError(
                    "(%s.%s) %s"
                    % (
                        orig.__class__.__module__,
                        orig.__class__.__name__,
                        orig,
                    ),
                    statement,
                    params,
                    orig,
                    hide_parameters=hide_parameters,
                    ismulti=ismulti,
                )

            glob = globals()
            for super_ in orig.__class__.__mro__:
                name = super_.__name__
                if dialect:
                    name = dialect.dbapi_exception_translation_map.get(
                        name, name
                    )
                if name in glob and issubclass(glob[name], DBAPIError):
                    cls = glob[name]
                    break

        return cls(
            statement,
            params,
            orig,
            connection_invalidated=connection_invalidated,
            hide_parameters=hide_parameters,
            code=cls.code,
            ismulti=ismulti,
        )

    def __reduce__(self):
        return (
            self.__class__,
            (
                self.statement,
                self.params,
                self.orig,
                self.hide_parameters,
                self.connection_invalidated,
                self.ismulti,
            ),
        )

    def __init__(
        self,
        statement,
        params,
        orig,
        hide_parameters=False,
        connection_invalidated=False,
        code=None,
        ismulti=None,
    ):
        try:
            text = str(orig)
        except Exception as e:
            text = "Error in str() of DB-API-generated exception: " + str(e)
        StatementError.__init__(
            self,
            "(%s.%s) %s"
            % (orig.__class__.__module__, orig.__class__.__name__, text),
            statement,
            params,
            orig,
            hide_parameters,
            code=code,
            ismulti=ismulti,
        )
        self.connection_invalidated = connection_invalidated


class InterfaceError(DBAPIError):
    """Wraps a DB-API InterfaceError."""

    code = "rvf5"


class DatabaseError(DBAPIError):
    """Wraps a DB-API DatabaseError."""

    code = "4xp6"


class DataError(DatabaseError):
    """Wraps a DB-API DataError."""

    code = "9h9h"


class OperationalError(DatabaseError):
    """Wraps a DB-API OperationalError."""

    code = "e3q8"


class IntegrityError(DatabaseError):
    """Wraps a DB-API IntegrityError."""

    code = "gkpj"


class InternalError(DatabaseError):
    """Wraps a DB-API InternalError."""

    code = "2j85"


class ProgrammingError(DatabaseError):
    """Wraps a DB-API ProgrammingError."""

    code = "f405"


class NotSupportedError(DatabaseError):
    """Wraps a DB-API NotSupportedError."""

    code = "tw8g"


# Warnings


class SADeprecationWarning(DeprecationWarning):
    """Issued for usage of deprecated APIs."""

    deprecated_since = None
    "Indicates the version that started raising this deprecation warning"


class RemovedIn20Warning(SADeprecationWarning):
    """Issued for usage of APIs specifically deprecated in SQLAlchemy 2.0.

    .. seealso::

        :ref:`error_b8d9`.

        :ref:`deprecation_20_mode`

    """

    deprecated_since = "1.4"
    "Indicates the version that started raising this deprecation warning"


class MovedIn20Warning(RemovedIn20Warning):
    """Subtype of RemovedIn20Warning to indicate an API that moved only."""


class SAPendingDeprecationWarning(PendingDeprecationWarning):
    """A similar warning as :class:`_exc.SADeprecationWarning`, this warning
    is not used in modern versions of SQLAlchemy.

    """

    deprecated_since = None
    "Indicates the version that started raising this deprecation warning"


class SAWarning(RuntimeWarning):
    """Issued at runtime."""
