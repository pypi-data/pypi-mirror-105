# sql/base.py
# Copyright (C) 2005-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""Foundational utilities common to many sql modules.

"""


import itertools
import operator
import re

from . import roles
from . import visitors
from .traversals import HasCacheKey  # noqa
from .traversals import HasCopyInternals  # noqa
from .traversals import MemoizedHasCacheKey  # noqa
from .visitors import ClauseVisitor
from .visitors import ExtendedInternalTraversal
from .visitors import InternalTraversal
from .. import exc
from .. import util
from ..util import HasMemoized
from ..util import hybridmethod

if util.TYPE_CHECKING:
    from types import ModuleType

coercions = None  # type: ModuleType
elements = None  # type: ModuleType
type_api = None  # type: ModuleType

PARSE_AUTOCOMMIT = util.symbol("PARSE_AUTOCOMMIT")
NO_ARG = util.symbol("NO_ARG")


class Immutable(object):
    """mark a ClauseElement as 'immutable' when expressions are cloned."""

    def unique_params(self, *optionaldict, **kwargs):
        raise NotImplementedError("Immutable objects do not support copying")

    def params(self, *optionaldict, **kwargs):
        raise NotImplementedError("Immutable objects do not support copying")

    def _clone(self, **kw):
        return self

    def _copy_internals(self, **kw):
        pass


class SingletonConstant(Immutable):
    """Represent SQL constants like NULL, TRUE, FALSE"""

    def __new__(cls, *arg, **kw):
        return cls._singleton

    @classmethod
    def _create_singleton(cls):
        obj = object.__new__(cls)
        obj.__init__()
        cls._singleton = obj

    # don't proxy singletons.   this means that a SingletonConstant
    # will never be a "corresponding column" in a statement; the constant
    # can be named directly and as it is often/usually compared against using
    # "IS", it can't be adapted to a subquery column in any case.
    # see :ticket:`6259`.
    proxy_set = frozenset()


def _from_objects(*elements):
    return itertools.chain.from_iterable(
        [element._from_objects for element in elements]
    )


def _select_iterables(elements):
    """expand tables into individual columns in the
    given list of column expressions.

    """
    return itertools.chain.from_iterable(
        [c._select_iterable for c in elements]
    )


def _generative(fn):
    """non-caching _generative() decorator.

    This is basically the legacy decorator that copies the object and
    runs a method on the new copy.

    """

    @util.decorator
    def _generative(fn, self, *args, **kw):
        """Mark a method as generative."""

        self = self._generate()
        x = fn(self, *args, **kw)
        assert x is None, "generative methods must have no return value"
        return self

    decorated = _generative(fn)
    decorated.non_generative = fn
    return decorated


def _exclusive_against(*names, **kw):
    msgs = kw.pop("msgs", {})

    defaults = kw.pop("defaults", {})

    getters = [
        (name, operator.attrgetter(name), defaults.get(name, None))
        for name in names
    ]

    @util.decorator
    def check(fn, self, *args, **kw):
        for name, getter, default_ in getters:
            if getter(self) is not default_:
                msg = msgs.get(
                    name,
                    "Method %s() has already been invoked on this %s construct"
                    % (fn.__name__, self.__class__),
                )
                raise exc.InvalidRequestError(msg)
        return fn(self, *args, **kw)

    return check


def _clone(element, **kw):
    return element._clone(**kw)


def _expand_cloned(elements):
    """expand the given set of ClauseElements to be the set of all 'cloned'
    predecessors.

    """
    return itertools.chain(*[x._cloned_set for x in elements])


def _cloned_intersection(a, b):
    """return the intersection of sets a and b, counting
    any overlap between 'cloned' predecessors.

    The returned set is in terms of the entities present within 'a'.

    """
    all_overlap = set(_expand_cloned(a)).intersection(_expand_cloned(b))
    return set(
        elem for elem in a if all_overlap.intersection(elem._cloned_set)
    )


def _cloned_difference(a, b):
    all_overlap = set(_expand_cloned(a)).intersection(_expand_cloned(b))
    return set(
        elem for elem in a if not all_overlap.intersection(elem._cloned_set)
    )


class _DialectArgView(util.collections_abc.MutableMapping):
    """A dictionary view of dialect-level arguments in the form
    <dialectname>_<argument_name>.

    """

    def __init__(self, obj):
        self.obj = obj

    def _key(self, key):
        try:
            dialect, value_key = key.split("_", 1)
        except ValueError as err:
            util.raise_(KeyError(key), replace_context=err)
        else:
            return dialect, value_key

    def __getitem__(self, key):
        dialect, value_key = self._key(key)

        try:
            opt = self.obj.dialect_options[dialect]
        except exc.NoSuchModuleError as err:
            util.raise_(KeyError(key), replace_context=err)
        else:
            return opt[value_key]

    def __setitem__(self, key, value):
        try:
            dialect, value_key = self._key(key)
        except KeyError as err:
            util.raise_(
                exc.ArgumentError(
                    "Keys must be of the form <dialectname>_<argname>"
                ),
                replace_context=err,
            )
        else:
            self.obj.dialect_options[dialect][value_key] = value

    def __delitem__(self, key):
        dialect, value_key = self._key(key)
        del self.obj.dialect_options[dialect][value_key]

    def __len__(self):
        return sum(
            len(args._non_defaults)
            for args in self.obj.dialect_options.values()
        )

    def __iter__(self):
        return (
            "%s_%s" % (dialect_name, value_name)
            for dialect_name in self.obj.dialect_options
            for value_name in self.obj.dialect_options[
                dialect_name
            ]._non_defaults
        )


class _DialectArgDict(util.collections_abc.MutableMapping):
    """A dictionary view of dialect-level arguments for a specific
    dialect.

    Maintains a separate collection of user-specified arguments
    and dialect-specified default arguments.

    """

    def __init__(self):
        self._non_defaults = {}
        self._defaults = {}

    def __len__(self):
        return len(set(self._non_defaults).union(self._defaults))

    def __iter__(self):
        return iter(set(self._non_defaults).union(self._defaults))

    def __getitem__(self, key):
        if key in self._non_defaults:
            return self._non_defaults[key]
        else:
            return self._defaults[key]

    def __setitem__(self, key, value):
        self._non_defaults[key] = value

    def __delitem__(self, key):
        del self._non_defaults[key]


@util.preload_module("sqlalchemy.dialects")
def _kw_reg_for_dialect(dialect_name):
    dialect_cls = util.preloaded.dialects.registry.load(dialect_name)
    if dialect_cls.construct_arguments is None:
        return None
    return dict(dialect_cls.construct_arguments)


class DialectKWArgs(object):
    """Establish the ability for a class to have dialect-specific arguments
    with defaults and constructor validation.

    The :class:`.DialectKWArgs` interacts with the
    :attr:`.DefaultDialect.construct_arguments` present on a dialect.

    .. seealso::

        :attr:`.DefaultDialect.construct_arguments`

    """

    _dialect_kwargs_traverse_internals = [
        ("dialect_options", InternalTraversal.dp_dialect_options)
    ]

    @classmethod
    def argument_for(cls, dialect_name, argument_name, default):
        """Add a new kind of dialect-specific keyword argument for this class.

        E.g.::

            Index.argument_for("mydialect", "length", None)

            some_index = Index('a', 'b', mydialect_length=5)

        The :meth:`.DialectKWArgs.argument_for` method is a per-argument
        way adding extra arguments to the
        :attr:`.DefaultDialect.construct_arguments` dictionary. This
        dictionary provides a list of argument names accepted by various
        schema-level constructs on behalf of a dialect.

        New dialects should typically specify this dictionary all at once as a
        data member of the dialect class.  The use case for ad-hoc addition of
        argument names is typically for end-user code that is also using
        a custom compilation scheme which consumes the additional arguments.

        :param dialect_name: name of a dialect.  The dialect must be
         locatable, else a :class:`.NoSuchModuleError` is raised.   The
         dialect must also include an existing
         :attr:`.DefaultDialect.construct_arguments` collection, indicating
         that it participates in the keyword-argument validation and default
         system, else :class:`.ArgumentError` is raised.  If the dialect does
         not include this collection, then any keyword argument can be
         specified on behalf of this dialect already.  All dialects packaged
         within SQLAlchemy include this collection, however for third party
         dialects, support may vary.

        :param argument_name: name of the parameter.

        :param default: default value of the parameter.

        .. versionadded:: 0.9.4

        """

        construct_arg_dictionary = DialectKWArgs._kw_registry[dialect_name]
        if construct_arg_dictionary is None:
            raise exc.ArgumentError(
                "Dialect '%s' does have keyword-argument "
                "validation and defaults enabled configured" % dialect_name
            )
        if cls not in construct_arg_dictionary:
            construct_arg_dictionary[cls] = {}
        construct_arg_dictionary[cls][argument_name] = default

    @util.memoized_property
    def dialect_kwargs(self):
        """A collection of keyword arguments specified as dialect-specific
        options to this construct.

        The arguments are present here in their original ``<dialect>_<kwarg>``
        format.  Only arguments that were actually passed are included;
        unlike the :attr:`.DialectKWArgs.dialect_options` collection, which
        contains all options known by this dialect including defaults.

        The collection is also writable; keys are accepted of the
        form ``<dialect>_<kwarg>`` where the value will be assembled
        into the list of options.

        .. versionadded:: 0.9.2

        .. versionchanged:: 0.9.4 The :attr:`.DialectKWArgs.dialect_kwargs`
           collection is now writable.

        .. seealso::

            :attr:`.DialectKWArgs.dialect_options` - nested dictionary form

        """
        return _DialectArgView(self)

    @property
    def kwargs(self):
        """A synonym for :attr:`.DialectKWArgs.dialect_kwargs`."""
        return self.dialect_kwargs

    _kw_registry = util.PopulateDict(_kw_reg_for_dialect)

    def _kw_reg_for_dialect_cls(self, dialect_name):
        construct_arg_dictionary = DialectKWArgs._kw_registry[dialect_name]
        d = _DialectArgDict()

        if construct_arg_dictionary is None:
            d._defaults.update({"*": None})
        else:
            for cls in reversed(self.__class__.__mro__):
                if cls in construct_arg_dictionary:
                    d._defaults.update(construct_arg_dictionary[cls])
        return d

    @util.memoized_property
    def dialect_options(self):
        """A collection of keyword arguments specified as dialect-specific
        options to this construct.

        This is a two-level nested registry, keyed to ``<dialect_name>``
        and ``<argument_name>``.  For example, the ``postgresql_where``
        argument would be locatable as::

            arg = my_object.dialect_options['postgresql']['where']

        .. versionadded:: 0.9.2

        .. seealso::

            :attr:`.DialectKWArgs.dialect_kwargs` - flat dictionary form

        """

        return util.PopulateDict(
            util.portable_instancemethod(self._kw_reg_for_dialect_cls)
        )

    def _validate_dialect_kwargs(self, kwargs):
        # validate remaining kwargs that they all specify DB prefixes

        if not kwargs:
            return

        for k in kwargs:
            m = re.match("^(.+?)_(.+)$", k)
            if not m:
                raise TypeError(
                    "Additional arguments should be "
                    "named <dialectname>_<argument>, got '%s'" % k
                )
            dialect_name, arg_name = m.group(1, 2)

            try:
                construct_arg_dictionary = self.dialect_options[dialect_name]
            except exc.NoSuchModuleError:
                util.warn(
                    "Can't validate argument %r; can't "
                    "locate any SQLAlchemy dialect named %r"
                    % (k, dialect_name)
                )
                self.dialect_options[dialect_name] = d = _DialectArgDict()
                d._defaults.update({"*": None})
                d._non_defaults[arg_name] = kwargs[k]
            else:
                if (
                    "*" not in construct_arg_dictionary
                    and arg_name not in construct_arg_dictionary
                ):
                    raise exc.ArgumentError(
                        "Argument %r is not accepted by "
                        "dialect %r on behalf of %r"
                        % (k, dialect_name, self.__class__)
                    )
                else:
                    construct_arg_dictionary[arg_name] = kwargs[k]


class CompileState(object):
    """Produces additional object state necessary for a statement to be
    compiled.

    the :class:`.CompileState` class is at the base of classes that assemble
    state for a particular statement object that is then used by the
    compiler.   This process is essentially an extension of the process that
    the SQLCompiler.visit_XYZ() method takes, however there is an emphasis
    on converting raw user intent into more organized structures rather than
    producing string output.   The top-level :class:`.CompileState` for the
    statement being executed is also accessible when the execution context
    works with invoking the statement and collecting results.

    The production of :class:`.CompileState` is specific to the compiler,  such
    as within the :meth:`.SQLCompiler.visit_insert`,
    :meth:`.SQLCompiler.visit_select` etc. methods.  These methods are also
    responsible for associating the :class:`.CompileState` with the
    :class:`.SQLCompiler` itself, if the statement is the "toplevel" statement,
    i.e. the outermost SQL statement that's actually being executed.
    There can be other :class:`.CompileState` objects that are not the
    toplevel, such as when a SELECT subquery or CTE-nested
    INSERT/UPDATE/DELETE is generated.

    .. versionadded:: 1.4

    """

    __slots__ = ("statement",)

    plugins = {}

    @classmethod
    def create_for_statement(cls, statement, compiler, **kw):
        # factory construction.

        if statement._propagate_attrs:
            plugin_name = statement._propagate_attrs.get(
                "compile_state_plugin", "default"
            )
            klass = cls.plugins.get(
                (plugin_name, statement._effective_plugin_target), None
            )
            if klass is None:
                klass = cls.plugins[
                    ("default", statement._effective_plugin_target)
                ]

        else:
            klass = cls.plugins[
                ("default", statement._effective_plugin_target)
            ]

        if klass is cls:
            return cls(statement, compiler, **kw)
        else:
            return klass.create_for_statement(statement, compiler, **kw)

    def __init__(self, statement, compiler, **kw):
        self.statement = statement

    @classmethod
    def get_plugin_class(cls, statement):
        plugin_name = statement._propagate_attrs.get(
            "compile_state_plugin", "default"
        )
        try:
            return cls.plugins[
                (plugin_name, statement._effective_plugin_target)
            ]
        except KeyError:
            return None

    @classmethod
    def _get_plugin_class_for_plugin(cls, statement, plugin_name):
        try:
            return cls.plugins[
                (plugin_name, statement._effective_plugin_target)
            ]
        except KeyError:
            return None

    @classmethod
    def plugin_for(cls, plugin_name, visit_name):
        def decorate(cls_to_decorate):
            cls.plugins[(plugin_name, visit_name)] = cls_to_decorate
            return cls_to_decorate

        return decorate


class Generative(HasMemoized):
    """Provide a method-chaining pattern in conjunction with the
    @_generative decorator."""

    def _generate(self):
        skip = self._memoized_keys
        cls = self.__class__
        s = cls.__new__(cls)
        if skip:
            s.__dict__ = {
                k: v for k, v in self.__dict__.items() if k not in skip
            }
        else:
            s.__dict__ = self.__dict__.copy()
        return s


class InPlaceGenerative(HasMemoized):
    """Provide a method-chaining pattern in conjunction with the
    @_generative decorator that mutates in place."""

    def _generate(self):
        skip = self._memoized_keys
        for k in skip:
            self.__dict__.pop(k, None)
        return self


class HasCompileState(Generative):
    """A class that has a :class:`.CompileState` associated with it."""

    _compile_state_plugin = None

    _attributes = util.immutabledict()

    _compile_state_factory = CompileState.create_for_statement


class _MetaOptions(type):
    """metaclass for the Options class."""

    def __init__(cls, classname, bases, dict_):
        cls._cache_attrs = tuple(
            sorted(
                d
                for d in dict_
                if not d.startswith("__")
                and d not in ("_cache_key_traversal",)
            )
        )
        type.__init__(cls, classname, bases, dict_)

    def __add__(self, other):
        o1 = self()

        if set(other).difference(self._cache_attrs):
            raise TypeError(
                "dictionary contains attributes not covered by "
                "Options class %s: %r"
                % (self, set(other).difference(self._cache_attrs))
            )

        o1.__dict__.update(other)
        return o1


class Options(util.with_metaclass(_MetaOptions)):
    """A cacheable option dictionary with defaults."""

    def __init__(self, **kw):
        self.__dict__.update(kw)

    def __add__(self, other):
        o1 = self.__class__.__new__(self.__class__)
        o1.__dict__.update(self.__dict__)

        if set(other).difference(self._cache_attrs):
            raise TypeError(
                "dictionary contains attributes not covered by "
                "Options class %s: %r"
                % (self, set(other).difference(self._cache_attrs))
            )

        o1.__dict__.update(other)
        return o1

    def __eq__(self, other):
        # TODO: very inefficient.  This is used only in test suites
        # right now.
        for a, b in util.zip_longest(self._cache_attrs, other._cache_attrs):
            if getattr(self, a) != getattr(other, b):
                return False
        return True

    def __repr__(self):
        # TODO: fairly inefficient, used only in debugging right now.

        return "%s(%s)" % (
            self.__class__.__name__,
            ", ".join(
                "%s=%r" % (k, self.__dict__[k])
                for k in self._cache_attrs
                if k in self.__dict__
            ),
        )

    @classmethod
    def isinstance(cls, klass):
        return issubclass(cls, klass)

    @hybridmethod
    def add_to_element(self, name, value):
        return self + {name: getattr(self, name) + value}

    @hybridmethod
    def _state_dict(self):
        return self.__dict__

    _state_dict_const = util.immutabledict()

    @_state_dict.classlevel
    def _state_dict(cls):
        return cls._state_dict_const

    @classmethod
    def safe_merge(cls, other):
        d = other._state_dict()

        # only support a merge with another object of our class
        # and which does not have attrs that we don't.   otherwise
        # we risk having state that might not be part of our cache
        # key strategy

        if (
            cls is not other.__class__
            and other._cache_attrs
            and set(other._cache_attrs).difference(cls._cache_attrs)
        ):
            raise TypeError(
                "other element %r is not empty, is not of type %s, "
                "and contains attributes not covered here %r"
                % (
                    other,
                    cls,
                    set(other._cache_attrs).difference(cls._cache_attrs),
                )
            )
        return cls + d

    @classmethod
    def from_execution_options(
        cls, key, attrs, exec_options, statement_exec_options
    ):
        """process Options argument in terms of execution options.


        e.g.::

            (
                load_options,
                execution_options,
            ) = QueryContext.default_load_options.from_execution_options(
                "_sa_orm_load_options",
                {
                    "populate_existing",
                    "autoflush",
                    "yield_per"
                },
                execution_options,
                statement._execution_options,
            )

        get back the Options and refresh "_sa_orm_load_options" in the
        exec options dict w/ the Options as well

        """

        # common case is that no options we are looking for are
        # in either dictionary, so cancel for that first
        check_argnames = attrs.intersection(
            set(exec_options).union(statement_exec_options)
        )

        existing_options = exec_options.get(key, cls)

        if check_argnames:
            result = {}
            for argname in check_argnames:
                local = "_" + argname
                if argname in exec_options:
                    result[local] = exec_options[argname]
                elif argname in statement_exec_options:
                    result[local] = statement_exec_options[argname]

            new_options = existing_options + result
            exec_options = util.immutabledict().merge_with(
                exec_options, {key: new_options}
            )
            return new_options, exec_options

        else:
            return existing_options, exec_options


class CacheableOptions(Options, HasCacheKey):
    @hybridmethod
    def _gen_cache_key(self, anon_map, bindparams):
        return HasCacheKey._gen_cache_key(self, anon_map, bindparams)

    @_gen_cache_key.classlevel
    def _gen_cache_key(cls, anon_map, bindparams):
        return (cls, ())

    @hybridmethod
    def _generate_cache_key(self):
        return HasCacheKey._generate_cache_key_for_object(self)


class ExecutableOption(HasCopyInternals, HasCacheKey):
    _annotations = util.EMPTY_DICT

    __visit_name__ = "executable_option"

    def _clone(self, **kw):
        """Create a shallow copy of this ExecutableOption."""
        c = self.__class__.__new__(self.__class__)
        c.__dict__ = dict(self.__dict__)
        return c


class Executable(roles.StatementRole, Generative):
    """Mark a :class:`_expression.ClauseElement` as supporting execution.

    :class:`.Executable` is a superclass for all "statement" types
    of objects, including :func:`select`, :func:`delete`, :func:`update`,
    :func:`insert`, :func:`text`.

    """

    supports_execution = True
    _execution_options = util.immutabledict()
    _bind = None
    _with_options = ()
    _with_context_options = ()

    _executable_traverse_internals = [
        ("_with_options", InternalTraversal.dp_executable_options),
        ("_with_context_options", ExtendedInternalTraversal.dp_plain_obj),
        ("_propagate_attrs", ExtendedInternalTraversal.dp_propagate_attrs),
    ]

    is_select = False
    is_update = False
    is_insert = False
    is_text = False
    is_delete = False
    is_dml = False

    @property
    def _effective_plugin_target(self):
        return self.__visit_name__

    @_generative
    def options(self, *options):
        """Apply options to this statement.

        In the general sense, options are any kind of Python object
        that can be interpreted by the SQL compiler for the statement.
        These options can be consumed by specific dialects or specific kinds
        of compilers.

        The most commonly known kind of option are the ORM level options
        that apply "eager load" and other loading behaviors to an ORM
        query.   However, options can theoretically be used for many other
        purposes.

        For background on specific kinds of options for specific kinds of
        statements, refer to the documentation for those option objects.

        .. versionchanged:: 1.4 - added :meth:`.Generative.options` to
           Core statement objects towards the goal of allowing unified
           Core / ORM querying capabilities.

        .. seealso::

            :ref:`deferred_options` - refers to options specific to the usage
            of ORM queries

            :ref:`relationship_loader_options` - refers to options specific
            to the usage of ORM queries

        """
        self._with_options += tuple(
            coercions.expect(roles.HasCacheKeyRole, opt) for opt in options
        )

    @_generative
    def _set_compile_options(self, compile_options):
        """Assign the compile options to a new value.

        :param compile_options: appropriate CacheableOptions structure

        """

        self._compile_options = compile_options

    @_generative
    def _update_compile_options(self, options):
        """update the _compile_options with new keys."""

        self._compile_options += options

    @_generative
    def _add_context_option(self, callable_, cache_args):
        """Add a context option to this statement.

        These are callable functions that will
        be given the CompileState object upon compilation.

        A second argument cache_args is required, which will be combined
        with the identity of the function itself in order to produce a
        cache key.

        """
        self._with_context_options += ((callable_, cache_args),)

    @_generative
    def execution_options(self, **kw):
        """Set non-SQL options for the statement which take effect during
        execution.

        Execution options can be set on a per-statement or
        per :class:`_engine.Connection` basis.   Additionally, the
        :class:`_engine.Engine` and ORM :class:`~.orm.query.Query`
        objects provide
        access to execution options which they in turn configure upon
        connections.

        The :meth:`execution_options` method is generative.  A new
        instance of this statement is returned that contains the options::

            statement = select(table.c.x, table.c.y)
            statement = statement.execution_options(autocommit=True)

        Note that only a subset of possible execution options can be applied
        to a statement - these include "autocommit" and "stream_results",
        but not "isolation_level" or "compiled_cache".
        See :meth:`_engine.Connection.execution_options` for a full list of
        possible options.

        .. seealso::

            :meth:`_engine.Connection.execution_options`

            :meth:`_query.Query.execution_options`

            :meth:`.Executable.get_execution_options`

        """
        if "isolation_level" in kw:
            raise exc.ArgumentError(
                "'isolation_level' execution option may only be specified "
                "on Connection.execution_options(), or "
                "per-engine using the isolation_level "
                "argument to create_engine()."
            )
        if "compiled_cache" in kw:
            raise exc.ArgumentError(
                "'compiled_cache' execution option may only be specified "
                "on Connection.execution_options(), not per statement."
            )
        self._execution_options = self._execution_options.union(kw)

    def get_execution_options(self):
        """Get the non-SQL options which will take effect during execution.

        .. versionadded:: 1.3

        .. seealso::

            :meth:`.Executable.execution_options`
        """
        return self._execution_options

    @util.deprecated_20(
        ":meth:`.Executable.execute`",
        alternative="All statement execution in SQLAlchemy 2.0 is performed "
        "by the :meth:`_engine.Connection.execute` method of "
        ":class:`_engine.Connection`, "
        "or in the ORM by the :meth:`.Session.execute` method of "
        ":class:`.Session`.",
    )
    def execute(self, *multiparams, **params):
        """Compile and execute this :class:`.Executable`."""
        e = self.bind
        if e is None:
            label = (
                getattr(self, "description", None) or self.__class__.__name__
            )
            msg = (
                "This %s is not directly bound to a Connection or Engine. "
                "Use the .execute() method of a Connection or Engine "
                "to execute this construct." % label
            )
            raise exc.UnboundExecutionError(msg)
        return e._execute_clauseelement(
            self, multiparams, params, util.immutabledict()
        )

    @util.deprecated_20(
        ":meth:`.Executable.scalar`",
        alternative="Scalar execution in SQLAlchemy 2.0 is performed "
        "by the :meth:`_engine.Connection.scalar` method of "
        ":class:`_engine.Connection`, "
        "or in the ORM by the :meth:`.Session.scalar` method of "
        ":class:`.Session`.",
    )
    def scalar(self, *multiparams, **params):
        """Compile and execute this :class:`.Executable`, returning the
        result's scalar representation.

        """
        return self.execute(*multiparams, **params).scalar()

    @property
    @util.deprecated_20(
        ":attr:`.Executable.bind`",
        alternative="Bound metadata is being removed as of SQLAlchemy 2.0.",
        enable_warnings=False,
    )
    def bind(self):
        """Returns the :class:`_engine.Engine` or :class:`_engine.Connection`
        to
        which this :class:`.Executable` is bound, or None if none found.

        This is a traversal which checks locally, then
        checks among the "from" clauses of associated objects
        until a bound engine or connection is found.

        """
        if self._bind is not None:
            return self._bind

        for f in _from_objects(self):
            if f is self:
                continue
            engine = f.bind
            if engine is not None:
                return engine
        else:
            return None


class prefix_anon_map(dict):
    """A map that creates new keys for missing key access.

    Considers keys of the form "<ident> <name>" to produce
    new symbols "<name>_<index>", where "index" is an incrementing integer
    corresponding to <name>.

    Inlines the approach taken by :class:`sqlalchemy.util.PopulateDict` which
    is otherwise usually used for this type of operation.

    """

    def __missing__(self, key):
        (ident, derived) = key.split(" ", 1)
        anonymous_counter = self.get(derived, 1)
        self[derived] = anonymous_counter + 1
        value = derived + "_" + str(anonymous_counter)
        self[key] = value
        return value


class SchemaEventTarget(object):
    """Base class for elements that are the targets of :class:`.DDLEvents`
    events.

    This includes :class:`.SchemaItem` as well as :class:`.SchemaType`.

    """

    def _set_parent(self, parent, **kw):
        """Associate with this SchemaEvent's parent object."""

    def _set_parent_with_dispatch(self, parent, **kw):
        self.dispatch.before_parent_attach(self, parent)
        self._set_parent(parent, **kw)
        self.dispatch.after_parent_attach(self, parent)


class SchemaVisitor(ClauseVisitor):
    """Define the visiting for ``SchemaItem`` objects."""

    __traverse_options__ = {"schema_visitor": True}


class ColumnCollection(object):
    """Collection of :class:`_expression.ColumnElement` instances,
    typically for
    selectables.

    The :class:`_expression.ColumnCollection`
    has both mapping- and sequence- like
    behaviors.   A :class:`_expression.ColumnCollection` usually stores
    :class:`_schema.Column`
    objects, which are then accessible both via mapping style access as well
    as attribute access style.  The name for which a :class:`_schema.Column`
    would
    be present is normally that of the :paramref:`_schema.Column.key`
    parameter,
    however depending on the context, it may be stored under a special label
    name::

        >>> from sqlalchemy import Column, Integer
        >>> from sqlalchemy.sql import ColumnCollection
        >>> x, y = Column('x', Integer), Column('y', Integer)
        >>> cc = ColumnCollection(columns=[(x.name, x), (y.name, y)])
        >>> cc.x
        Column('x', Integer(), table=None)
        >>> cc.y
        Column('y', Integer(), table=None)
        >>> cc['x']
        Column('x', Integer(), table=None)
        >>> cc['y']

    :class:`.ColumnCollection` also indexes the columns in order and allows
    them to be accessible by their integer position::

        >>> cc[0]
        Column('x', Integer(), table=None)
        >>> cc[1]
        Column('y', Integer(), table=None)

    .. versionadded:: 1.4 :class:`_expression.ColumnCollection`
       allows integer-based
       index access to the collection.

    Iterating the collection yields the column expressions in order::

        >>> list(cc)
        [Column('x', Integer(), table=None),
         Column('y', Integer(), table=None)]

    The base :class:`_expression.ColumnCollection` object can store
    duplicates, which can
    mean either two columns with the same key, in which case the column
    returned by key  access is **arbitrary**::

        >>> x1, x2 = Column('x', Integer), Column('x', Integer)
        >>> cc = ColumnCollection(columns=[(x1.name, x1), (x2.name, x2)])
        >>> list(cc)
        [Column('x', Integer(), table=None),
         Column('x', Integer(), table=None)]
        >>> cc['x'] is x1
        False
        >>> cc['x'] is x2
        True

    Or it can also mean the same column multiple times.   These cases are
    supported as :class:`_expression.ColumnCollection`
    is used to represent the columns in
    a SELECT statement which may include duplicates.

    A special subclass :class:`.DedupeColumnCollection` exists which instead
    maintains SQLAlchemy's older behavior of not allowing duplicates; this
    collection is used for schema level objects like :class:`_schema.Table`
    and
    :class:`.PrimaryKeyConstraint` where this deduping is helpful.  The
    :class:`.DedupeColumnCollection` class also has additional mutation methods
    as the schema constructs have more use cases that require removal and
    replacement of columns.

    .. versionchanged:: 1.4 :class:`_expression.ColumnCollection`
       now stores duplicate
       column keys as well as the same column in multiple positions.  The
       :class:`.DedupeColumnCollection` class is added to maintain the
       former behavior in those cases where deduplication as well as
       additional replace/remove operations are needed.


    """

    __slots__ = "_collection", "_index", "_colset"

    def __init__(self, columns=None):
        object.__setattr__(self, "_colset", set())
        object.__setattr__(self, "_index", {})
        object.__setattr__(self, "_collection", [])
        if columns:
            self._initial_populate(columns)

    def _initial_populate(self, iter_):
        self._populate_separate_keys(iter_)

    @property
    def _all_columns(self):
        return [col for (k, col) in self._collection]

    def keys(self):
        return [k for (k, col) in self._collection]

    def values(self):
        return [col for (k, col) in self._collection]

    def items(self):
        return list(self._collection)

    def __bool__(self):
        return bool(self._collection)

    def __len__(self):
        return len(self._collection)

    def __iter__(self):
        # turn to a list first to maintain over a course of changes
        return iter([col for k, col in self._collection])

    def __getitem__(self, key):
        try:
            return self._index[key]
        except KeyError as err:
            if isinstance(key, util.int_types):
                util.raise_(IndexError(key), replace_context=err)
            else:
                raise

    def __getattr__(self, key):
        try:
            return self._index[key]
        except KeyError as err:
            util.raise_(AttributeError(key), replace_context=err)

    def __contains__(self, key):
        if key not in self._index:
            if not isinstance(key, util.string_types):
                raise exc.ArgumentError(
                    "__contains__ requires a string argument"
                )
            return False
        else:
            return True

    def compare(self, other):
        for l, r in util.zip_longest(self, other):
            if l is not r:
                return False
        else:
            return True

    def __eq__(self, other):
        return self.compare(other)

    def get(self, key, default=None):
        if key in self._index:
            return self._index[key]
        else:
            return default

    def __str__(self):
        return "%s(%s)" % (
            self.__class__.__name__,
            ", ".join(str(c) for c in self),
        )

    def __setitem__(self, key, value):
        raise NotImplementedError()

    def __delitem__(self, key):
        raise NotImplementedError()

    def __setattr__(self, key, obj):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()

    def remove(self, column):
        raise NotImplementedError()

    def update(self, iter_):
        raise NotImplementedError()

    __hash__ = None

    def _populate_separate_keys(self, iter_):
        """populate from an iterator of (key, column)"""
        cols = list(iter_)
        self._collection[:] = cols
        self._colset.update(c for k, c in self._collection)
        self._index.update(
            (idx, c) for idx, (k, c) in enumerate(self._collection)
        )
        self._index.update({k: col for k, col in reversed(self._collection)})

    def add(self, column, key=None):
        if key is None:
            key = column.key

        l = len(self._collection)
        self._collection.append((key, column))
        self._colset.add(column)
        self._index[l] = column
        if key not in self._index:
            self._index[key] = column

    def __getstate__(self):
        return {"_collection": self._collection, "_index": self._index}

    def __setstate__(self, state):
        object.__setattr__(self, "_index", state["_index"])
        object.__setattr__(self, "_collection", state["_collection"])
        object.__setattr__(
            self, "_colset", {col for k, col in self._collection}
        )

    def contains_column(self, col):
        """Checks if a column object exists in this collection"""
        if col not in self._colset:
            if isinstance(col, util.string_types):
                raise exc.ArgumentError(
                    "contains_column cannot be used with string arguments. "
                    "Use ``col_name in table.c`` instead."
                )
            return False
        else:
            return True

    def as_immutable(self):
        return ImmutableColumnCollection(self)

    def corresponding_column(self, column, require_embedded=False):
        """Given a :class:`_expression.ColumnElement`, return the exported
        :class:`_expression.ColumnElement` object from this
        :class:`_expression.ColumnCollection`
        which corresponds to that original :class:`_expression.ColumnElement`
        via a common
        ancestor column.

        :param column: the target :class:`_expression.ColumnElement`
                      to be matched.

        :param require_embedded: only return corresponding columns for
         the given :class:`_expression.ColumnElement`, if the given
         :class:`_expression.ColumnElement`
         is actually present within a sub-element
         of this :class:`_expression.Selectable`.
         Normally the column will match if
         it merely shares a common ancestor with one of the exported
         columns of this :class:`_expression.Selectable`.

        .. seealso::

            :meth:`_expression.Selectable.corresponding_column`
            - invokes this method
            against the collection returned by
            :attr:`_expression.Selectable.exported_columns`.

        .. versionchanged:: 1.4 the implementation for ``corresponding_column``
           was moved onto the :class:`_expression.ColumnCollection` itself.

        """

        def embedded(expanded_proxy_set, target_set):
            for t in target_set.difference(expanded_proxy_set):
                if not set(_expand_cloned([t])).intersection(
                    expanded_proxy_set
                ):
                    return False
            return True

        # don't dig around if the column is locally present
        if column in self._colset:
            return column
        col, intersect = None, None
        target_set = column.proxy_set
        cols = [c for (k, c) in self._collection]
        for c in cols:
            expanded_proxy_set = set(_expand_cloned(c.proxy_set))
            i = target_set.intersection(expanded_proxy_set)
            if i and (
                not require_embedded
                or embedded(expanded_proxy_set, target_set)
            ):
                if col is None:

                    # no corresponding column yet, pick this one.

                    col, intersect = c, i
                elif len(i) > len(intersect):

                    # 'c' has a larger field of correspondence than
                    # 'col'. i.e. selectable.c.a1_x->a1.c.x->table.c.x
                    # matches a1.c.x->table.c.x better than
                    # selectable.c.x->table.c.x does.

                    col, intersect = c, i
                elif i == intersect:
                    # they have the same field of correspondence. see
                    # which proxy_set has fewer columns in it, which
                    # indicates a closer relationship with the root
                    # column. Also take into account the "weight"
                    # attribute which CompoundSelect() uses to give
                    # higher precedence to columns based on vertical
                    # position in the compound statement, and discard
                    # columns that have no reference to the target
                    # column (also occurs with CompoundSelect)

                    col_distance = util.reduce(
                        operator.add,
                        [
                            sc._annotations.get("weight", 1)
                            for sc in col._uncached_proxy_set()
                            if sc.shares_lineage(column)
                        ],
                    )
                    c_distance = util.reduce(
                        operator.add,
                        [
                            sc._annotations.get("weight", 1)
                            for sc in c._uncached_proxy_set()
                            if sc.shares_lineage(column)
                        ],
                    )
                    if c_distance < col_distance:
                        col, intersect = c, i
        return col


class DedupeColumnCollection(ColumnCollection):
    """A :class:`_expression.ColumnCollection`
    that maintains deduplicating behavior.

    This is useful by schema level objects such as :class:`_schema.Table` and
    :class:`.PrimaryKeyConstraint`.    The collection includes more
    sophisticated mutator methods as well to suit schema objects which
    require mutable column collections.

    .. versionadded:: 1.4

    """

    def add(self, column, key=None):

        if key is not None and column.key != key:
            raise exc.ArgumentError(
                "DedupeColumnCollection requires columns be under "
                "the same key as their .key"
            )
        key = column.key

        if key is None:
            raise exc.ArgumentError(
                "Can't add unnamed column to column collection"
            )

        if key in self._index:

            existing = self._index[key]

            if existing is column:
                return

            self.replace(column)

            # pop out memoized proxy_set as this
            # operation may very well be occurring
            # in a _make_proxy operation
            util.memoized_property.reset(column, "proxy_set")
        else:
            l = len(self._collection)
            self._collection.append((key, column))
            self._colset.add(column)
            self._index[l] = column
            self._index[key] = column

    def _populate_separate_keys(self, iter_):
        """populate from an iterator of (key, column)"""
        cols = list(iter_)

        replace_col = []
        for k, col in cols:
            if col.key != k:
                raise exc.ArgumentError(
                    "DedupeColumnCollection requires columns be under "
                    "the same key as their .key"
                )
            if col.name in self._index and col.key != col.name:
                replace_col.append(col)
            elif col.key in self._index:
                replace_col.append(col)
            else:
                self._index[k] = col
                self._collection.append((k, col))
        self._colset.update(c for (k, c) in self._collection)
        self._index.update(
            (idx, c) for idx, (k, c) in enumerate(self._collection)
        )
        for col in replace_col:
            self.replace(col)

    def extend(self, iter_):
        self._populate_separate_keys((col.key, col) for col in iter_)

    def remove(self, column):
        if column not in self._colset:
            raise ValueError(
                "Can't remove column %r; column is not in this collection"
                % column
            )
        del self._index[column.key]
        self._colset.remove(column)
        self._collection[:] = [
            (k, c) for (k, c) in self._collection if c is not column
        ]
        self._index.update(
            {idx: col for idx, (k, col) in enumerate(self._collection)}
        )
        # delete higher index
        del self._index[len(self._collection)]

    def replace(self, column):
        """add the given column to this collection, removing unaliased
        versions of this column  as well as existing columns with the
        same key.

        e.g.::

            t = Table('sometable', metadata, Column('col1', Integer))
            t.columns.replace(Column('col1', Integer, key='columnone'))

        will remove the original 'col1' from the collection, and add
        the new column under the name 'columnname'.

        Used by schema.Column to override columns during table reflection.

        """

        remove_col = set()
        # remove up to two columns based on matches of name as well as key
        if column.name in self._index and column.key != column.name:
            other = self._index[column.name]
            if other.name == other.key:
                remove_col.add(other)

        if column.key in self._index:
            remove_col.add(self._index[column.key])

        new_cols = []
        replaced = False
        for k, col in self._collection:
            if col in remove_col:
                if not replaced:
                    replaced = True
                    new_cols.append((column.key, column))
            else:
                new_cols.append((k, col))

        if remove_col:
            self._colset.difference_update(remove_col)

        if not replaced:
            new_cols.append((column.key, column))

        self._colset.add(column)
        self._collection[:] = new_cols

        self._index.clear()
        self._index.update(
            {idx: col for idx, (k, col) in enumerate(self._collection)}
        )
        self._index.update(self._collection)


class ImmutableColumnCollection(util.ImmutableContainer, ColumnCollection):
    __slots__ = ("_parent",)

    def __init__(self, collection):
        object.__setattr__(self, "_parent", collection)
        object.__setattr__(self, "_colset", collection._colset)
        object.__setattr__(self, "_index", collection._index)
        object.__setattr__(self, "_collection", collection._collection)

    def __getstate__(self):
        return {"_parent": self._parent}

    def __setstate__(self, state):
        parent = state["_parent"]
        self.__init__(parent)

    add = extend = remove = util.ImmutableContainer._immutable


class ColumnSet(util.ordered_column_set):
    def contains_column(self, col):
        return col in self

    def extend(self, cols):
        for col in cols:
            self.add(col)

    def __add__(self, other):
        return list(self) + list(other)

    def __eq__(self, other):
        l = []
        for c in other:
            for local in self:
                if c.shares_lineage(local):
                    l.append(c == local)
        return elements.and_(*l)

    def __hash__(self):
        return hash(tuple(x for x in self))


def _bind_or_error(schemaitem, msg=None):

    util.warn_deprecated_20(
        "The ``bind`` argument for schema methods that invoke SQL "
        "against an engine or connection will be required in SQLAlchemy 2.0."
    )
    bind = schemaitem.bind
    if not bind:
        name = schemaitem.__class__.__name__
        label = getattr(
            schemaitem, "fullname", getattr(schemaitem, "name", None)
        )
        if label:
            item = "%s object %r" % (name, label)
        else:
            item = "%s object" % name
        if msg is None:
            msg = (
                "%s is not bound to an Engine or Connection.  "
                "Execution can not proceed without a database to execute "
                "against." % item
            )
        raise exc.UnboundExecutionError(msg)
    return bind


def _entity_namespace(entity):
    """Return the nearest .entity_namespace for the given entity.

    If not immediately available, does an iterate to find a sub-element
    that has one, if any.

    """
    try:
        return entity.entity_namespace
    except AttributeError:
        for elem in visitors.iterate(entity):
            if hasattr(elem, "entity_namespace"):
                return elem.entity_namespace
        else:
            raise


def _entity_namespace_key(entity, key):
    """Return an entry from an entity_namespace.


    Raises :class:`_exc.InvalidRequestError` rather than attribute error
    on not found.

    """

    try:
        ns = _entity_namespace(entity)
        return getattr(ns, key)
    except AttributeError as err:
        util.raise_(
            exc.InvalidRequestError(
                'Entity namespace for "%s" has no property "%s"'
                % (entity, key)
            ),
            replace_context=err,
        )
