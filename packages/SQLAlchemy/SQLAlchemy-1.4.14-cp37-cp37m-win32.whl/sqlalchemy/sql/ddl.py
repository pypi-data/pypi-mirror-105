# sql/ddl.py
# Copyright (C) 2009-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
"""
Provides the hierarchy of DDL-defining schema items as well as routines
to invoke them for a create/drop call.

"""

from . import roles
from .base import _bind_or_error
from .base import _generative
from .base import Executable
from .base import SchemaVisitor
from .elements import ClauseElement
from .. import exc
from .. import util
from ..util import topological


class _DDLCompiles(ClauseElement):
    def _compiler(self, dialect, **kw):
        """Return a compiler appropriate for this ClauseElement, given a
        Dialect."""

        return dialect.ddl_compiler(dialect, self, **kw)

    def _compile_w_cache(self, *arg, **kw):
        raise NotImplementedError()


class DDLElement(roles.DDLRole, Executable, _DDLCompiles):
    """Base class for DDL expression constructs.

    This class is the base for the general purpose :class:`.DDL` class,
    as well as the various create/drop clause constructs such as
    :class:`.CreateTable`, :class:`.DropTable`, :class:`.AddConstraint`,
    etc.

    :class:`.DDLElement` integrates closely with SQLAlchemy events,
    introduced in :ref:`event_toplevel`.  An instance of one is
    itself an event receiving callable::

        event.listen(
            users,
            'after_create',
            AddConstraint(constraint).execute_if(dialect='postgresql')
        )

    .. seealso::

        :class:`.DDL`

        :class:`.DDLEvents`

        :ref:`event_toplevel`

        :ref:`schema_ddl_sequences`

    """

    _execution_options = Executable._execution_options.union(
        {"autocommit": True}
    )

    target = None
    on = None
    dialect = None
    callable_ = None

    def _execute_on_connection(
        self, connection, multiparams, params, execution_options
    ):
        return connection._execute_ddl(
            self, multiparams, params, execution_options
        )

    @util.deprecated_20(
        ":meth:`.DDLElement.execute`",
        alternative="All statement execution in SQLAlchemy 2.0 is performed "
        "by the :meth:`_engine.Connection.execute` method of "
        ":class:`_engine.Connection`, "
        "or in the ORM by the :meth:`.Session.execute` method of "
        ":class:`.Session`.",
    )
    def execute(self, bind=None, target=None):
        """Execute this DDL immediately.

        Executes the DDL statement in isolation using the supplied
        :class:`.Connectable` or
        :class:`.Connectable` assigned to the ``.bind``
        property, if not supplied. If the DDL has a conditional ``on``
        criteria, it will be invoked with None as the event.

        :param bind:
          Optional, an ``Engine`` or ``Connection``. If not supplied, a valid
          :class:`.Connectable` must be present in the
          ``.bind`` property.

        :param target:
          Optional, defaults to None.  The target :class:`_schema.SchemaItem`
          for the execute call.   This is equivalent to passing the
          :class:`_schema.SchemaItem` to the :meth:`.DDLElement.against`
          method and then invoking :meth:`_schema.DDLElement.execute`
          upon the resulting :class:`_schema.DDLElement` object.  See
          :meth:`.DDLElement.against` for further detail.

        """

        if bind is None:
            bind = _bind_or_error(self)

        if self._should_execute(target, bind):
            return bind.execute(self.against(target))
        else:
            bind.engine.logger.info("DDL execution skipped, criteria not met.")

    @_generative
    def against(self, target):
        """Return a copy of this :class:`_schema.DDLElement` which will include
        the given target.

        This essentially applies the given item to the ``.target`` attribute
        of the returned :class:`_schema.DDLElement` object.  This target
        is then usable by event handlers and compilation routines in order to
        provide services such as tokenization of a DDL string in terms of a
        particular :class:`_schema.Table`.

        When a :class:`_schema.DDLElement` object is established as an event
        handler for the :meth:`_events.DDLEvents.before_create` or
        :meth:`_events.DDLEvents.after_create` events, and the event
        then occurs for a given target such as a :class:`_schema.Constraint`
        or :class:`_schema.Table`, that target is established with a copy
        of the :class:`_schema.DDLElement` object using this method, which
        then proceeds to the :meth:`_schema.DDLElement.execute` method
        in order to invoke the actual DDL instruction.

        :param target: a :class:`_schema.SchemaItem` that will be the subject
         of a DDL operation.

        :return: a copy of this :class:`_schema.DDLElement` with the
         ``.target`` attribute assigned to the given
         :class:`_schema.SchemaItem`.

        .. seealso::

            :class:`_schema.DDL` - uses tokenization against the "target" when
            processing the DDL string.

        """

        self.target = target

    @_generative
    def execute_if(self, dialect=None, callable_=None, state=None):
        r"""Return a callable that will execute this
        :class:`_ddl.DDLElement` conditionally within an event handler.

        Used to provide a wrapper for event listening::

            event.listen(
                        metadata,
                        'before_create',
                        DDL("my_ddl").execute_if(dialect='postgresql')
                    )

        :param dialect: May be a string or tuple of strings.
          If a string, it will be compared to the name of the
          executing database dialect::

            DDL('something').execute_if(dialect='postgresql')

          If a tuple, specifies multiple dialect names::

            DDL('something').execute_if(dialect=('postgresql', 'mysql'))

        :param callable\_: A callable, which will be invoked with
          four positional arguments as well as optional keyword
          arguments:

            :ddl:
              This DDL element.

            :target:
              The :class:`_schema.Table` or :class:`_schema.MetaData`
              object which is the
              target of this event. May be None if the DDL is executed
              explicitly.

            :bind:
              The :class:`_engine.Connection` being used for DDL execution

            :tables:
              Optional keyword argument - a list of Table objects which are to
              be created/ dropped within a MetaData.create_all() or drop_all()
              method call.

            :state:
              Optional keyword argument - will be the ``state`` argument
              passed to this function.

            :checkfirst:
             Keyword argument, will be True if the 'checkfirst' flag was
             set during the call to ``create()``, ``create_all()``,
             ``drop()``, ``drop_all()``.

          If the callable returns a True value, the DDL statement will be
          executed.

        :param state: any value which will be passed to the callable\_
          as the ``state`` keyword argument.

        .. seealso::

            :class:`.DDLEvents`

            :ref:`event_toplevel`

        """
        self.dialect = dialect
        self.callable_ = callable_
        self.state = state

    def _should_execute(self, target, bind, **kw):
        if isinstance(self.dialect, util.string_types):
            if self.dialect != bind.engine.name:
                return False
        elif isinstance(self.dialect, (tuple, list, set)):
            if bind.engine.name not in self.dialect:
                return False
        if self.callable_ is not None and not self.callable_(
            self, target, bind, state=self.state, **kw
        ):
            return False

        return True

    def __call__(self, target, bind, **kw):
        """Execute the DDL as a ddl_listener."""

        if self._should_execute(target, bind, **kw):
            return bind.execute(self.against(target))

    def bind(self):
        if self._bind:
            return self._bind

    def _set_bind(self, bind):
        self._bind = bind

    bind = property(bind, _set_bind)

    def _generate(self):
        s = self.__class__.__new__(self.__class__)
        s.__dict__ = self.__dict__.copy()
        return s


class DDL(DDLElement):
    """A literal DDL statement.

    Specifies literal SQL DDL to be executed by the database.  DDL objects
    function as DDL event listeners, and can be subscribed to those events
    listed in :class:`.DDLEvents`, using either :class:`_schema.Table` or
    :class:`_schema.MetaData` objects as targets.
    Basic templating support allows
    a single DDL instance to handle repetitive tasks for multiple tables.

    Examples::

      from sqlalchemy import event, DDL

      tbl = Table('users', metadata, Column('uid', Integer))
      event.listen(tbl, 'before_create', DDL('DROP TRIGGER users_trigger'))

      spow = DDL('ALTER TABLE %(table)s SET secretpowers TRUE')
      event.listen(tbl, 'after_create', spow.execute_if(dialect='somedb'))

      drop_spow = DDL('ALTER TABLE users SET secretpowers FALSE')
      connection.execute(drop_spow)

    When operating on Table events, the following ``statement``
    string substitutions are available::

      %(table)s  - the Table name, with any required quoting applied
      %(schema)s - the schema name, with any required quoting applied
      %(fullname)s - the Table name including schema, quoted if needed

    The DDL's "context", if any, will be combined with the standard
    substitutions noted above.  Keys present in the context will override
    the standard substitutions.

    """

    __visit_name__ = "ddl"

    @util.deprecated_params(
        bind=(
            "2.0",
            "The :paramref:`_ddl.DDL.bind` argument is deprecated and "
            "will be removed in SQLAlchemy 2.0.",
        ),
    )
    def __init__(self, statement, context=None, bind=None):
        """Create a DDL statement.

        :param statement:
          A string or unicode string to be executed.  Statements will be
          processed with Python's string formatting operator.  See the
          ``context`` argument and the ``execute_at`` method.

          A literal '%' in a statement must be escaped as '%%'.

          SQL bind parameters are not available in DDL statements.

        :param context:
          Optional dictionary, defaults to None.  These values will be
          available for use in string substitutions on the DDL statement.

        :param bind:
          Optional. A :class:`.Connectable`, used by
          default when ``execute()`` is invoked without a bind argument.


        .. seealso::

            :class:`.DDLEvents`

            :ref:`event_toplevel`

        """

        if not isinstance(statement, util.string_types):
            raise exc.ArgumentError(
                "Expected a string or unicode SQL statement, got '%r'"
                % statement
            )

        self.statement = statement
        self.context = context or {}

        self._bind = bind

    def __repr__(self):
        return "<%s@%s; %s>" % (
            type(self).__name__,
            id(self),
            ", ".join(
                [repr(self.statement)]
                + [
                    "%s=%r" % (key, getattr(self, key))
                    for key in ("on", "context")
                    if getattr(self, key)
                ]
            ),
        )


class _CreateDropBase(DDLElement):
    """Base class for DDL constructs that represent CREATE and DROP or
    equivalents.

    The common theme of _CreateDropBase is a single
    ``element`` attribute which refers to the element
    to be created or dropped.

    """

    @util.deprecated_params(
        bind=(
            "2.0",
            "The :paramref:`_ddl.DDLElement.bind` argument is "
            "deprecated and "
            "will be removed in SQLAlchemy 2.0.",
        ),
    )
    def __init__(
        self,
        element,
        bind=None,
        if_exists=False,
        if_not_exists=False,
        _legacy_bind=None,
    ):
        self.element = element
        if bind:
            self.bind = bind
        elif _legacy_bind:
            self.bind = _legacy_bind
        self.if_exists = if_exists
        self.if_not_exists = if_not_exists

    @property
    def stringify_dialect(self):
        return self.element.create_drop_stringify_dialect

    def _create_rule_disable(self, compiler):
        """Allow disable of _create_rule using a callable.

        Pass to _create_rule using
        util.portable_instancemethod(self._create_rule_disable)
        to retain serializability.

        """
        return False


class CreateSchema(_CreateDropBase):
    """Represent a CREATE SCHEMA statement.

    The argument here is the string name of the schema.

    """

    __visit_name__ = "create_schema"

    def __init__(self, name, quote=None, **kw):
        """Create a new :class:`.CreateSchema` construct."""

        self.quote = quote
        super(CreateSchema, self).__init__(name, **kw)


class DropSchema(_CreateDropBase):
    """Represent a DROP SCHEMA statement.

    The argument here is the string name of the schema.

    """

    __visit_name__ = "drop_schema"

    def __init__(self, name, quote=None, cascade=False, **kw):
        """Create a new :class:`.DropSchema` construct."""

        self.quote = quote
        self.cascade = cascade
        super(DropSchema, self).__init__(name, **kw)


class CreateTable(_CreateDropBase):
    """Represent a CREATE TABLE statement."""

    __visit_name__ = "create_table"

    @util.deprecated_params(
        bind=(
            "2.0",
            "The :paramref:`_ddl.CreateTable.bind` argument is deprecated and "
            "will be removed in SQLAlchemy 2.0.",
        ),
    )
    def __init__(
        self,
        element,
        bind=None,
        include_foreign_key_constraints=None,
        if_not_exists=False,
    ):
        """Create a :class:`.CreateTable` construct.

        :param element: a :class:`_schema.Table` that's the subject
         of the CREATE
        :param on: See the description for 'on' in :class:`.DDL`.
        :param bind: See the description for 'bind' in :class:`.DDL`.
        :param include_foreign_key_constraints: optional sequence of
         :class:`_schema.ForeignKeyConstraint` objects that will be included
         inline within the CREATE construct; if omitted, all foreign key
         constraints that do not specify use_alter=True are included.

         .. versionadded:: 1.0.0

        :param if_not_exists: if True, an IF NOT EXISTS operator will be
         applied to the construct.

         .. versionadded:: 1.4.0b2

        """
        super(CreateTable, self).__init__(
            element, _legacy_bind=bind, if_not_exists=if_not_exists
        )
        self.columns = [CreateColumn(column) for column in element.columns]
        self.include_foreign_key_constraints = include_foreign_key_constraints


class _DropView(_CreateDropBase):
    """Semi-public 'DROP VIEW' construct.

    Used by the test suite for dialect-agnostic drops of views.
    This object will eventually be part of a public "view" API.

    """

    __visit_name__ = "drop_view"


class CreateColumn(_DDLCompiles):
    """Represent a :class:`_schema.Column`
    as rendered in a CREATE TABLE statement,
    via the :class:`.CreateTable` construct.

    This is provided to support custom column DDL within the generation
    of CREATE TABLE statements, by using the
    compiler extension documented in :ref:`sqlalchemy.ext.compiler_toplevel`
    to extend :class:`.CreateColumn`.

    Typical integration is to examine the incoming :class:`_schema.Column`
    object, and to redirect compilation if a particular flag or condition
    is found::

        from sqlalchemy import schema
        from sqlalchemy.ext.compiler import compiles

        @compiles(schema.CreateColumn)
        def compile(element, compiler, **kw):
            column = element.element

            if "special" not in column.info:
                return compiler.visit_create_column(element, **kw)

            text = "%s SPECIAL DIRECTIVE %s" % (
                    column.name,
                    compiler.type_compiler.process(column.type)
                )
            default = compiler.get_column_default_string(column)
            if default is not None:
                text += " DEFAULT " + default

            if not column.nullable:
                text += " NOT NULL"

            if column.constraints:
                text += " ".join(
                            compiler.process(const)
                            for const in column.constraints)
            return text

    The above construct can be applied to a :class:`_schema.Table`
    as follows::

        from sqlalchemy import Table, Metadata, Column, Integer, String
        from sqlalchemy import schema

        metadata = MetaData()

        table = Table('mytable', MetaData(),
                Column('x', Integer, info={"special":True}, primary_key=True),
                Column('y', String(50)),
                Column('z', String(20), info={"special":True})
            )

        metadata.create_all(conn)

    Above, the directives we've added to the :attr:`_schema.Column.info`
    collection
    will be detected by our custom compilation scheme::

        CREATE TABLE mytable (
                x SPECIAL DIRECTIVE INTEGER NOT NULL,
                y VARCHAR(50),
                z SPECIAL DIRECTIVE VARCHAR(20),
            PRIMARY KEY (x)
        )

    The :class:`.CreateColumn` construct can also be used to skip certain
    columns when producing a ``CREATE TABLE``.  This is accomplished by
    creating a compilation rule that conditionally returns ``None``.
    This is essentially how to produce the same effect as using the
    ``system=True`` argument on :class:`_schema.Column`, which marks a column
    as an implicitly-present "system" column.

    For example, suppose we wish to produce a :class:`_schema.Table`
    which skips
    rendering of the PostgreSQL ``xmin`` column against the PostgreSQL
    backend, but on other backends does render it, in anticipation of a
    triggered rule.  A conditional compilation rule could skip this name only
    on PostgreSQL::

        from sqlalchemy.schema import CreateColumn

        @compiles(CreateColumn, "postgresql")
        def skip_xmin(element, compiler, **kw):
            if element.element.name == 'xmin':
                return None
            else:
                return compiler.visit_create_column(element, **kw)


        my_table = Table('mytable', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('xmin', Integer)
                )

    Above, a :class:`.CreateTable` construct will generate a ``CREATE TABLE``
    which only includes the ``id`` column in the string; the ``xmin`` column
    will be omitted, but only against the PostgreSQL backend.

    """

    __visit_name__ = "create_column"

    def __init__(self, element):
        self.element = element


class DropTable(_CreateDropBase):
    """Represent a DROP TABLE statement."""

    __visit_name__ = "drop_table"

    @util.deprecated_params(
        bind=(
            "2.0",
            "The :paramref:`_ddl.DropTable.bind` argument is "
            "deprecated and "
            "will be removed in SQLAlchemy 2.0.",
        ),
    )
    def __init__(self, element, bind=None, if_exists=False):
        """Create a :class:`.DropTable` construct.

        :param element: a :class:`_schema.Table` that's the subject
         of the DROP.
        :param on: See the description for 'on' in :class:`.DDL`.
        :param bind: See the description for 'bind' in :class:`.DDL`.
        :param if_exists: if True, an IF EXISTS operator will be applied to the
         construct.

         .. versionadded:: 1.4.0b2

        """
        super(DropTable, self).__init__(
            element, _legacy_bind=bind, if_exists=if_exists
        )


class CreateSequence(_CreateDropBase):
    """Represent a CREATE SEQUENCE statement."""

    __visit_name__ = "create_sequence"


class DropSequence(_CreateDropBase):
    """Represent a DROP SEQUENCE statement."""

    __visit_name__ = "drop_sequence"


class CreateIndex(_CreateDropBase):
    """Represent a CREATE INDEX statement."""

    __visit_name__ = "create_index"

    @util.deprecated_params(
        bind=(
            "2.0",
            "The :paramref:`_ddl.CreateIndex.bind` argument is "
            "deprecated and "
            "will be removed in SQLAlchemy 2.0.",
        ),
    )
    def __init__(self, element, bind=None, if_not_exists=False):
        """Create a :class:`.Createindex` construct.

        :param element: a :class:`_schema.Index` that's the subject
         of the CREATE.
        :param on: See the description for 'on' in :class:`.DDL`.
        :param bind: See the description for 'bind' in :class:`.DDL`.
        :param if_not_exists: if True, an IF NOT EXISTS operator will be
         applied to the construct.

         .. versionadded:: 1.4.0b2

        """
        super(CreateIndex, self).__init__(
            element, _legacy_bind=bind, if_not_exists=if_not_exists
        )


class DropIndex(_CreateDropBase):
    """Represent a DROP INDEX statement."""

    __visit_name__ = "drop_index"

    @util.deprecated_params(
        bind=(
            "2.0",
            "The :paramref:`_ddl.DropIndex.bind` argument is "
            "deprecated and "
            "will be removed in SQLAlchemy 2.0.",
        ),
    )
    def __init__(self, element, bind=None, if_exists=False):
        """Create a :class:`.DropIndex` construct.

        :param element: a :class:`_schema.Index` that's the subject
         of the DROP.
        :param on: See the description for 'on' in :class:`.DDL`.
        :param bind: See the description for 'bind' in :class:`.DDL`.
        :param if_exists: if True, an IF EXISTS operator will be applied to the
         construct.

         .. versionadded:: 1.4.0b2

        """
        super(DropIndex, self).__init__(
            element, _legacy_bind=bind, if_exists=if_exists
        )


class AddConstraint(_CreateDropBase):
    """Represent an ALTER TABLE ADD CONSTRAINT statement."""

    __visit_name__ = "add_constraint"

    def __init__(self, element, *args, **kw):
        super(AddConstraint, self).__init__(element, *args, **kw)
        element._create_rule = util.portable_instancemethod(
            self._create_rule_disable
        )


class DropConstraint(_CreateDropBase):
    """Represent an ALTER TABLE DROP CONSTRAINT statement."""

    __visit_name__ = "drop_constraint"

    def __init__(self, element, cascade=False, **kw):
        self.cascade = cascade
        super(DropConstraint, self).__init__(element, **kw)
        element._create_rule = util.portable_instancemethod(
            self._create_rule_disable
        )


class SetTableComment(_CreateDropBase):
    """Represent a COMMENT ON TABLE IS statement."""

    __visit_name__ = "set_table_comment"


class DropTableComment(_CreateDropBase):
    """Represent a COMMENT ON TABLE '' statement.

    Note this varies a lot across database backends.

    """

    __visit_name__ = "drop_table_comment"


class SetColumnComment(_CreateDropBase):
    """Represent a COMMENT ON COLUMN IS statement."""

    __visit_name__ = "set_column_comment"


class DropColumnComment(_CreateDropBase):
    """Represent a COMMENT ON COLUMN IS NULL statement."""

    __visit_name__ = "drop_column_comment"


class DDLBase(SchemaVisitor):
    def __init__(self, connection):
        self.connection = connection


class SchemaGenerator(DDLBase):
    def __init__(
        self, dialect, connection, checkfirst=False, tables=None, **kwargs
    ):
        super(SchemaGenerator, self).__init__(connection, **kwargs)
        self.checkfirst = checkfirst
        self.tables = tables
        self.preparer = dialect.identifier_preparer
        self.dialect = dialect
        self.memo = {}

    def _can_create_table(self, table):
        self.dialect.validate_identifier(table.name)
        effective_schema = self.connection.schema_for_object(table)
        if effective_schema:
            self.dialect.validate_identifier(effective_schema)
        return not self.checkfirst or not self.dialect.has_table(
            self.connection, table.name, schema=effective_schema
        )

    def _can_create_index(self, index):
        effective_schema = self.connection.schema_for_object(index.table)
        if effective_schema:
            self.dialect.validate_identifier(effective_schema)
        return not self.checkfirst or not self.dialect.has_index(
            self.connection,
            index.table.name,
            index.name,
            schema=effective_schema,
        )

    def _can_create_sequence(self, sequence):
        effective_schema = self.connection.schema_for_object(sequence)

        return self.dialect.supports_sequences and (
            (not self.dialect.sequences_optional or not sequence.optional)
            and (
                not self.checkfirst
                or not self.dialect.has_sequence(
                    self.connection, sequence.name, schema=effective_schema
                )
            )
        )

    def visit_metadata(self, metadata):
        if self.tables is not None:
            tables = self.tables
        else:
            tables = list(metadata.tables.values())

        collection = sort_tables_and_constraints(
            [t for t in tables if self._can_create_table(t)]
        )

        seq_coll = [
            s
            for s in metadata._sequences.values()
            if s.column is None and self._can_create_sequence(s)
        ]

        event_collection = [t for (t, fks) in collection if t is not None]
        metadata.dispatch.before_create(
            metadata,
            self.connection,
            tables=event_collection,
            checkfirst=self.checkfirst,
            _ddl_runner=self,
        )

        for seq in seq_coll:
            self.traverse_single(seq, create_ok=True)

        for table, fkcs in collection:
            if table is not None:
                self.traverse_single(
                    table,
                    create_ok=True,
                    include_foreign_key_constraints=fkcs,
                    _is_metadata_operation=True,
                )
            else:
                for fkc in fkcs:
                    self.traverse_single(fkc)

        metadata.dispatch.after_create(
            metadata,
            self.connection,
            tables=event_collection,
            checkfirst=self.checkfirst,
            _ddl_runner=self,
        )

    def visit_table(
        self,
        table,
        create_ok=False,
        include_foreign_key_constraints=None,
        _is_metadata_operation=False,
    ):
        if not create_ok and not self._can_create_table(table):
            return

        table.dispatch.before_create(
            table,
            self.connection,
            checkfirst=self.checkfirst,
            _ddl_runner=self,
            _is_metadata_operation=_is_metadata_operation,
        )

        for column in table.columns:
            if column.default is not None:
                self.traverse_single(column.default)

        if not self.dialect.supports_alter:
            # e.g., don't omit any foreign key constraints
            include_foreign_key_constraints = None

        self.connection.execute(
            # fmt: off
            CreateTable(
                table,
                include_foreign_key_constraints=  # noqa
                    include_foreign_key_constraints,  # noqa
            )
            # fmt: on
        )

        if hasattr(table, "indexes"):
            for index in table.indexes:
                self.traverse_single(index, create_ok=True)

        if self.dialect.supports_comments and not self.dialect.inline_comments:
            if table.comment is not None:
                self.connection.execute(SetTableComment(table))

            for column in table.columns:
                if column.comment is not None:
                    self.connection.execute(SetColumnComment(column))

        table.dispatch.after_create(
            table,
            self.connection,
            checkfirst=self.checkfirst,
            _ddl_runner=self,
            _is_metadata_operation=_is_metadata_operation,
        )

    def visit_foreign_key_constraint(self, constraint):
        if not self.dialect.supports_alter:
            return
        self.connection.execute(AddConstraint(constraint))

    def visit_sequence(self, sequence, create_ok=False):
        if not create_ok and not self._can_create_sequence(sequence):
            return
        self.connection.execute(CreateSequence(sequence))

    def visit_index(self, index, create_ok=False):
        if not create_ok and not self._can_create_index(index):
            return
        self.connection.execute(CreateIndex(index))


class SchemaDropper(DDLBase):
    def __init__(
        self, dialect, connection, checkfirst=False, tables=None, **kwargs
    ):
        super(SchemaDropper, self).__init__(connection, **kwargs)
        self.checkfirst = checkfirst
        self.tables = tables
        self.preparer = dialect.identifier_preparer
        self.dialect = dialect
        self.memo = {}

    def visit_metadata(self, metadata):
        if self.tables is not None:
            tables = self.tables
        else:
            tables = list(metadata.tables.values())

        try:
            unsorted_tables = [t for t in tables if self._can_drop_table(t)]
            collection = list(
                reversed(
                    sort_tables_and_constraints(
                        unsorted_tables,
                        filter_fn=lambda constraint: False
                        if not self.dialect.supports_alter
                        or constraint.name is None
                        else None,
                    )
                )
            )
        except exc.CircularDependencyError as err2:
            if not self.dialect.supports_alter:
                util.warn(
                    "Can't sort tables for DROP; an "
                    "unresolvable foreign key "
                    "dependency exists between tables: %s; and backend does "
                    "not support ALTER.  To restore at least a partial sort, "
                    "apply use_alter=True to ForeignKey and "
                    "ForeignKeyConstraint "
                    "objects involved in the cycle to mark these as known "
                    "cycles that will be ignored."
                    % (", ".join(sorted([t.fullname for t in err2.cycles])))
                )
                collection = [(t, ()) for t in unsorted_tables]
            else:
                util.raise_(
                    exc.CircularDependencyError(
                        err2.args[0],
                        err2.cycles,
                        err2.edges,
                        msg="Can't sort tables for DROP; an "
                        "unresolvable foreign key "
                        "dependency exists between tables: %s.  Please ensure "
                        "that the ForeignKey and ForeignKeyConstraint objects "
                        "involved in the cycle have "
                        "names so that they can be dropped using "
                        "DROP CONSTRAINT."
                        % (
                            ", ".join(
                                sorted([t.fullname for t in err2.cycles])
                            )
                        ),
                    ),
                    from_=err2,
                )

        seq_coll = [
            s
            for s in metadata._sequences.values()
            if self._can_drop_sequence(s)
        ]

        event_collection = [t for (t, fks) in collection if t is not None]

        metadata.dispatch.before_drop(
            metadata,
            self.connection,
            tables=event_collection,
            checkfirst=self.checkfirst,
            _ddl_runner=self,
        )

        for table, fkcs in collection:
            if table is not None:
                self.traverse_single(
                    table,
                    drop_ok=True,
                    _is_metadata_operation=True,
                    _ignore_sequences=seq_coll,
                )
            else:
                for fkc in fkcs:
                    self.traverse_single(fkc)

        for seq in seq_coll:
            self.traverse_single(seq, drop_ok=seq.column is None)

        metadata.dispatch.after_drop(
            metadata,
            self.connection,
            tables=event_collection,
            checkfirst=self.checkfirst,
            _ddl_runner=self,
        )

    def _can_drop_table(self, table):
        self.dialect.validate_identifier(table.name)
        effective_schema = self.connection.schema_for_object(table)
        if effective_schema:
            self.dialect.validate_identifier(effective_schema)
        return not self.checkfirst or self.dialect.has_table(
            self.connection, table.name, schema=effective_schema
        )

    def _can_drop_index(self, index):
        effective_schema = self.connection.schema_for_object(index.table)
        if effective_schema:
            self.dialect.validate_identifier(effective_schema)
        return not self.checkfirst or self.dialect.has_index(
            self.connection,
            index.table.name,
            index.name,
            schema=effective_schema,
        )

    def _can_drop_sequence(self, sequence):
        effective_schema = self.connection.schema_for_object(sequence)
        return self.dialect.supports_sequences and (
            (not self.dialect.sequences_optional or not sequence.optional)
            and (
                not self.checkfirst
                or self.dialect.has_sequence(
                    self.connection, sequence.name, schema=effective_schema
                )
            )
        )

    def visit_index(self, index, drop_ok=False):
        if not drop_ok and not self._can_drop_index(index):
            return

        self.connection.execute(DropIndex(index))

    def visit_table(
        self,
        table,
        drop_ok=False,
        _is_metadata_operation=False,
        _ignore_sequences=[],
    ):
        if not drop_ok and not self._can_drop_table(table):
            return

        table.dispatch.before_drop(
            table,
            self.connection,
            checkfirst=self.checkfirst,
            _ddl_runner=self,
            _is_metadata_operation=_is_metadata_operation,
        )

        self.connection.execute(DropTable(table))

        # traverse client side defaults which may refer to server-side
        # sequences. noting that some of these client side defaults may also be
        # set up as server side defaults (see http://docs.sqlalchemy.org/en/
        # latest/core/defaults.html#associating-a-sequence-as-the-server-side-
        # default), so have to be dropped after the table is dropped.
        for column in table.columns:
            if (
                column.default is not None
                and column.default not in _ignore_sequences
            ):
                self.traverse_single(column.default)

        table.dispatch.after_drop(
            table,
            self.connection,
            checkfirst=self.checkfirst,
            _ddl_runner=self,
            _is_metadata_operation=_is_metadata_operation,
        )

    def visit_foreign_key_constraint(self, constraint):
        if not self.dialect.supports_alter:
            return
        self.connection.execute(DropConstraint(constraint))

    def visit_sequence(self, sequence, drop_ok=False):

        if not drop_ok and not self._can_drop_sequence(sequence):
            return
        self.connection.execute(DropSequence(sequence))


def sort_tables(
    tables,
    skip_fn=None,
    extra_dependencies=None,
):
    """Sort a collection of :class:`_schema.Table` objects based on
    dependency.

    This is a dependency-ordered sort which will emit :class:`_schema.Table`
    objects such that they will follow their dependent :class:`_schema.Table`
    objects.
    Tables are dependent on another based on the presence of
    :class:`_schema.ForeignKeyConstraint`
    objects as well as explicit dependencies
    added by :meth:`_schema.Table.add_is_dependent_on`.

    .. warning::

        The :func:`._schema.sort_tables` function cannot by itself
        accommodate automatic resolution of dependency cycles between
        tables, which are usually caused by mutually dependent foreign key
        constraints. When these cycles are detected, the foreign keys
        of these tables are omitted from consideration in the sort.
        A warning is emitted when this condition occurs, which will be an
        exception raise in a future release.   Tables which are not part
        of the cycle will still be returned in dependency order.

        To resolve these cycles, the
        :paramref:`_schema.ForeignKeyConstraint.use_alter` parameter may be
        applied to those constraints which create a cycle.  Alternatively,
        the :func:`_schema.sort_tables_and_constraints` function will
        automatically return foreign key constraints in a separate
        collection when cycles are detected so that they may be applied
        to a schema separately.

        .. versionchanged:: 1.3.17 - a warning is emitted when
           :func:`_schema.sort_tables` cannot perform a proper sort due to
           cyclical dependencies.  This will be an exception in a future
           release.  Additionally, the sort will continue to return
           other tables not involved in the cycle in dependency order
           which was not the case previously.

    :param tables: a sequence of :class:`_schema.Table` objects.

    :param skip_fn: optional callable which will be passed a
     :class:`_schema.ForeignKey` object; if it returns True, this
     constraint will not be considered as a dependency.  Note this is
     **different** from the same parameter in
     :func:`.sort_tables_and_constraints`, which is
     instead passed the owning :class:`_schema.ForeignKeyConstraint` object.

    :param extra_dependencies: a sequence of 2-tuples of tables which will
     also be considered as dependent on each other.

    .. seealso::

        :func:`.sort_tables_and_constraints`

        :attr:`_schema.MetaData.sorted_tables` - uses this function to sort


    """

    if skip_fn is not None:

        def _skip_fn(fkc):
            for fk in fkc.elements:
                if skip_fn(fk):
                    return True
            else:
                return None

    else:
        _skip_fn = None

    return [
        t
        for (t, fkcs) in sort_tables_and_constraints(
            tables,
            filter_fn=_skip_fn,
            extra_dependencies=extra_dependencies,
            _warn_for_cycles=True,
        )
        if t is not None
    ]


def sort_tables_and_constraints(
    tables, filter_fn=None, extra_dependencies=None, _warn_for_cycles=False
):
    """Sort a collection of :class:`_schema.Table`  /
    :class:`_schema.ForeignKeyConstraint`
    objects.

    This is a dependency-ordered sort which will emit tuples of
    ``(Table, [ForeignKeyConstraint, ...])`` such that each
    :class:`_schema.Table` follows its dependent :class:`_schema.Table`
    objects.
    Remaining :class:`_schema.ForeignKeyConstraint`
    objects that are separate due to
    dependency rules not satisfied by the sort are emitted afterwards
    as ``(None, [ForeignKeyConstraint ...])``.

    Tables are dependent on another based on the presence of
    :class:`_schema.ForeignKeyConstraint` objects, explicit dependencies
    added by :meth:`_schema.Table.add_is_dependent_on`,
    as well as dependencies
    stated here using the :paramref:`~.sort_tables_and_constraints.skip_fn`
    and/or :paramref:`~.sort_tables_and_constraints.extra_dependencies`
    parameters.

    :param tables: a sequence of :class:`_schema.Table` objects.

    :param filter_fn: optional callable which will be passed a
     :class:`_schema.ForeignKeyConstraint` object,
     and returns a value based on
     whether this constraint should definitely be included or excluded as
     an inline constraint, or neither.   If it returns False, the constraint
     will definitely be included as a dependency that cannot be subject
     to ALTER; if True, it will **only** be included as an ALTER result at
     the end.   Returning None means the constraint is included in the
     table-based result unless it is detected as part of a dependency cycle.

    :param extra_dependencies: a sequence of 2-tuples of tables which will
     also be considered as dependent on each other.

    .. versionadded:: 1.0.0

    .. seealso::

        :func:`.sort_tables`


    """

    fixed_dependencies = set()
    mutable_dependencies = set()

    if extra_dependencies is not None:
        fixed_dependencies.update(extra_dependencies)

    remaining_fkcs = set()
    for table in tables:
        for fkc in table.foreign_key_constraints:
            if fkc.use_alter is True:
                remaining_fkcs.add(fkc)
                continue

            if filter_fn:
                filtered = filter_fn(fkc)

                if filtered is True:
                    remaining_fkcs.add(fkc)
                    continue

            dependent_on = fkc.referred_table
            if dependent_on is not table:
                mutable_dependencies.add((dependent_on, table))

        fixed_dependencies.update(
            (parent, table) for parent in table._extra_dependencies
        )

    try:
        candidate_sort = list(
            topological.sort(
                fixed_dependencies.union(mutable_dependencies),
                tables,
            )
        )
    except exc.CircularDependencyError as err:
        if _warn_for_cycles:
            util.warn(
                "Cannot correctly sort tables; there are unresolvable cycles "
                'between tables "%s", which is usually caused by mutually '
                "dependent foreign key constraints.  Foreign key constraints "
                "involving these tables will not be considered; this warning "
                "may raise an error in a future release."
                % (", ".join(sorted(t.fullname for t in err.cycles)),)
            )
        for edge in err.edges:
            if edge in mutable_dependencies:
                table = edge[1]
                if table not in err.cycles:
                    continue
                can_remove = [
                    fkc
                    for fkc in table.foreign_key_constraints
                    if filter_fn is None or filter_fn(fkc) is not False
                ]
                remaining_fkcs.update(can_remove)
                for fkc in can_remove:
                    dependent_on = fkc.referred_table
                    if dependent_on is not table:
                        mutable_dependencies.discard((dependent_on, table))
        candidate_sort = list(
            topological.sort(
                fixed_dependencies.union(mutable_dependencies),
                tables,
            )
        )

    return [
        (table, table.foreign_key_constraints.difference(remaining_fkcs))
        for table in candidate_sort
    ] + [(None, list(remaining_fkcs))]
