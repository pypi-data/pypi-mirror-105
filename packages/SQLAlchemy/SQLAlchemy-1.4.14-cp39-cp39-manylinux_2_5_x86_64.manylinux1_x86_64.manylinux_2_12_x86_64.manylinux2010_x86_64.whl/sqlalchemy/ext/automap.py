# ext/automap.py
# Copyright (C) 2005-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

r"""Define an extension to the :mod:`sqlalchemy.ext.declarative` system
which automatically generates mapped classes and relationships from a database
schema, typically though not necessarily one which is reflected.

.. versionadded:: 0.9.1 Added :mod:`sqlalchemy.ext.automap`.

It is hoped that the :class:`.AutomapBase` system provides a quick
and modernized solution to the problem that the very famous
`SQLSoup <https://sqlsoup.readthedocs.io/en/latest/>`_
also tries to solve, that of generating a quick and rudimentary object
model from an existing database on the fly.  By addressing the issue strictly
at the mapper configuration level, and integrating fully with existing
Declarative class techniques, :class:`.AutomapBase` seeks to provide
a well-integrated approach to the issue of expediently auto-generating ad-hoc
mappings.


Basic Use
=========

The simplest usage is to reflect an existing database into a new model.
We create a new :class:`.AutomapBase` class in a similar manner as to how
we create a declarative base class, using :func:`.automap_base`.
We then call :meth:`.AutomapBase.prepare` on the resulting base class,
asking it to reflect the schema and produce mappings::

    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy.orm import Session
    from sqlalchemy import create_engine

    Base = automap_base()

    # engine, suppose it has two tables 'user' and 'address' set up
    engine = create_engine("sqlite:///mydatabase.db")

    # reflect the tables
    Base.prepare(engine, reflect=True)

    # mapped classes are now created with names by default
    # matching that of the table name.
    User = Base.classes.user
    Address = Base.classes.address

    session = Session(engine)

    # rudimentary relationships are produced
    session.add(Address(email_address="foo@bar.com", user=User(name="foo")))
    session.commit()

    # collection-based relationships are by default named
    # "<classname>_collection"
    print (u1.address_collection)

Above, calling :meth:`.AutomapBase.prepare` while passing along the
:paramref:`.AutomapBase.prepare.reflect` parameter indicates that the
:meth:`_schema.MetaData.reflect`
method will be called on this declarative base
classes' :class:`_schema.MetaData` collection; then, each **viable**
:class:`_schema.Table` within the :class:`_schema.MetaData`
will get a new mapped class
generated automatically.  The :class:`_schema.ForeignKeyConstraint`
objects which
link the various tables together will be used to produce new, bidirectional
:func:`_orm.relationship` objects between classes.
The classes and relationships
follow along a default naming scheme that we can customize.  At this point,
our basic mapping consisting of related ``User`` and ``Address`` classes is
ready to use in the traditional way.

.. note:: By **viable**, we mean that for a table to be mapped, it must
   specify a primary key.  Additionally, if the table is detected as being
   a pure association table between two other tables, it will not be directly
   mapped and will instead be configured as a many-to-many table between
   the mappings for the two referring tables.

Generating Mappings from an Existing MetaData
=============================================

We can pass a pre-declared :class:`_schema.MetaData` object to
:func:`.automap_base`.
This object can be constructed in any way, including programmatically, from
a serialized file, or from itself being reflected using
:meth:`_schema.MetaData.reflect`.
Below we illustrate a combination of reflection and
explicit table declaration::

    from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey
    from sqlalchemy.ext.automap import automap_base
    engine = create_engine("sqlite:///mydatabase.db")

    # produce our own MetaData object
    metadata = MetaData()

    # we can reflect it ourselves from a database, using options
    # such as 'only' to limit what tables we look at...
    metadata.reflect(engine, only=['user', 'address'])

    # ... or just define our own Table objects with it (or combine both)
    Table('user_order', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('user_id', ForeignKey('user.id'))
                )

    # we can then produce a set of mappings from this MetaData.
    Base = automap_base(metadata=metadata)

    # calling prepare() just sets up mapped classes and relationships.
    Base.prepare()

    # mapped classes are ready
    User, Address, Order = Base.classes.user, Base.classes.address,\
        Base.classes.user_order

Specifying Classes Explicitly
=============================

The :mod:`.sqlalchemy.ext.automap` extension allows classes to be defined
explicitly, in a way similar to that of the :class:`.DeferredReflection` class.
Classes that extend from :class:`.AutomapBase` act like regular declarative
classes, but are not immediately mapped after their construction, and are
instead mapped when we call :meth:`.AutomapBase.prepare`.  The
:meth:`.AutomapBase.prepare` method will make use of the classes we've
established based on the table name we use.  If our schema contains tables
``user`` and ``address``, we can define one or both of the classes to be used::

    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy import create_engine

    # automap base
    Base = automap_base()

    # pre-declare User for the 'user' table
    class User(Base):
        __tablename__ = 'user'

        # override schema elements like Columns
        user_name = Column('name', String)

        # override relationships too, if desired.
        # we must use the same name that automap would use for the
        # relationship, and also must refer to the class name that automap will
        # generate for "address"
        address_collection = relationship("address", collection_class=set)

    # reflect
    engine = create_engine("sqlite:///mydatabase.db")
    Base.prepare(engine, reflect=True)

    # we still have Address generated from the tablename "address",
    # but User is the same as Base.classes.User now

    Address = Base.classes.address

    u1 = session.query(User).first()
    print (u1.address_collection)

    # the backref is still there:
    a1 = session.query(Address).first()
    print (a1.user)

Above, one of the more intricate details is that we illustrated overriding
one of the :func:`_orm.relationship` objects that automap would have created.
To do this, we needed to make sure the names match up with what automap
would normally generate, in that the relationship name would be
``User.address_collection`` and the name of the class referred to, from
automap's perspective, is called ``address``, even though we are referring to
it as ``Address`` within our usage of this class.

Overriding Naming Schemes
=========================

:mod:`.sqlalchemy.ext.automap` is tasked with producing mapped classes and
relationship names based on a schema, which means it has decision points in how
these names are determined.  These three decision points are provided using
functions which can be passed to the :meth:`.AutomapBase.prepare` method, and
are known as :func:`.classname_for_table`,
:func:`.name_for_scalar_relationship`,
and :func:`.name_for_collection_relationship`.  Any or all of these
functions are provided as in the example below, where we use a "camel case"
scheme for class names and a "pluralizer" for collection names using the
`Inflect <https://pypi.python.org/pypi/inflect>`_ package::

    import re
    import inflect

    def camelize_classname(base, tablename, table):
        "Produce a 'camelized' class name, e.g. "
        "'words_and_underscores' -> 'WordsAndUnderscores'"

        return str(tablename[0].upper() + \
                re.sub(r'_([a-z])', lambda m: m.group(1).upper(), tablename[1:]))

    _pluralizer = inflect.engine()
    def pluralize_collection(base, local_cls, referred_cls, constraint):
        "Produce an 'uncamelized', 'pluralized' class name, e.g. "
        "'SomeTerm' -> 'some_terms'"

        referred_name = referred_cls.__name__
        uncamelized = re.sub(r'[A-Z]',
                             lambda m: "_%s" % m.group(0).lower(),
                             referred_name)[1:]
        pluralized = _pluralizer.plural(uncamelized)
        return pluralized

    from sqlalchemy.ext.automap import automap_base

    Base = automap_base()

    engine = create_engine("sqlite:///mydatabase.db")

    Base.prepare(engine, reflect=True,
                classname_for_table=camelize_classname,
                name_for_collection_relationship=pluralize_collection
        )

From the above mapping, we would now have classes ``User`` and ``Address``,
where the collection from ``User`` to ``Address`` is called
``User.addresses``::

    User, Address = Base.classes.User, Base.classes.Address

    u1 = User(addresses=[Address(email="foo@bar.com")])

Relationship Detection
======================

The vast majority of what automap accomplishes is the generation of
:func:`_orm.relationship` structures based on foreign keys.  The mechanism
by which this works for many-to-one and one-to-many relationships is as
follows:

1. A given :class:`_schema.Table`, known to be mapped to a particular class,
   is examined for :class:`_schema.ForeignKeyConstraint` objects.

2. From each :class:`_schema.ForeignKeyConstraint`, the remote
   :class:`_schema.Table`
   object present is matched up to the class to which it is to be mapped,
   if any, else it is skipped.

3. As the :class:`_schema.ForeignKeyConstraint`
   we are examining corresponds to a
   reference from the immediate mapped class,  the relationship will be set up
   as a many-to-one referring to the referred class; a corresponding
   one-to-many backref will be created on the referred class referring
   to this class.

4. If any of the columns that are part of the
   :class:`_schema.ForeignKeyConstraint`
   are not nullable (e.g. ``nullable=False``), a
   :paramref:`_orm.relationship.cascade` keyword argument
   of ``all, delete-orphan`` will be added to the keyword arguments to
   be passed to the relationship or backref.  If the
   :class:`_schema.ForeignKeyConstraint` reports that
   :paramref:`_schema.ForeignKeyConstraint.ondelete`
   is set to ``CASCADE`` for a not null or ``SET NULL`` for a nullable
   set of columns, the option :paramref:`_orm.relationship.passive_deletes`
   flag is set to ``True`` in the set of relationship keyword arguments.
   Note that not all backends support reflection of ON DELETE.

   .. versionadded:: 1.0.0 - automap will detect non-nullable foreign key
      constraints when producing a one-to-many relationship and establish
      a default cascade of ``all, delete-orphan`` if so; additionally,
      if the constraint specifies
      :paramref:`_schema.ForeignKeyConstraint.ondelete`
      of ``CASCADE`` for non-nullable or ``SET NULL`` for nullable columns,
      the ``passive_deletes=True`` option is also added.

5. The names of the relationships are determined using the
   :paramref:`.AutomapBase.prepare.name_for_scalar_relationship` and
   :paramref:`.AutomapBase.prepare.name_for_collection_relationship`
   callable functions.  It is important to note that the default relationship
   naming derives the name from the **the actual class name**.  If you've
   given a particular class an explicit name by declaring it, or specified an
   alternate class naming scheme, that's the name from which the relationship
   name will be derived.

6. The classes are inspected for an existing mapped property matching these
   names.  If one is detected on one side, but none on the other side,
   :class:`.AutomapBase` attempts to create a relationship on the missing side,
   then uses the :paramref:`_orm.relationship.back_populates`
   parameter in order to
   point the new relationship to the other side.

7. In the usual case where no relationship is on either side,
   :meth:`.AutomapBase.prepare` produces a :func:`_orm.relationship` on the
   "many-to-one" side and matches it to the other using the
   :paramref:`_orm.relationship.backref` parameter.

8. Production of the :func:`_orm.relationship` and optionally the
   :func:`.backref`
   is handed off to the :paramref:`.AutomapBase.prepare.generate_relationship`
   function, which can be supplied by the end-user in order to augment
   the arguments passed to :func:`_orm.relationship` or :func:`.backref` or to
   make use of custom implementations of these functions.

Custom Relationship Arguments
-----------------------------

The :paramref:`.AutomapBase.prepare.generate_relationship` hook can be used
to add parameters to relationships.  For most cases, we can make use of the
existing :func:`.automap.generate_relationship` function to return
the object, after augmenting the given keyword dictionary with our own
arguments.

Below is an illustration of how to send
:paramref:`_orm.relationship.cascade` and
:paramref:`_orm.relationship.passive_deletes`
options along to all one-to-many relationships::

    from sqlalchemy.ext.automap import generate_relationship

    def _gen_relationship(base, direction, return_fn,
                                    attrname, local_cls, referred_cls, **kw):
        if direction is interfaces.ONETOMANY:
            kw['cascade'] = 'all, delete-orphan'
            kw['passive_deletes'] = True
        # make use of the built-in function to actually return
        # the result.
        return generate_relationship(base, direction, return_fn,
                                     attrname, local_cls, referred_cls, **kw)

    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy import create_engine

    # automap base
    Base = automap_base()

    engine = create_engine("sqlite:///mydatabase.db")
    Base.prepare(engine, reflect=True,
                generate_relationship=_gen_relationship)

Many-to-Many relationships
--------------------------

:mod:`.sqlalchemy.ext.automap` will generate many-to-many relationships, e.g.
those which contain a ``secondary`` argument.  The process for producing these
is as follows:

1. A given :class:`_schema.Table` is examined for
   :class:`_schema.ForeignKeyConstraint`
   objects, before any mapped class has been assigned to it.

2. If the table contains two and exactly two
   :class:`_schema.ForeignKeyConstraint`
   objects, and all columns within this table are members of these two
   :class:`_schema.ForeignKeyConstraint` objects, the table is assumed to be a
   "secondary" table, and will **not be mapped directly**.

3. The two (or one, for self-referential) external tables to which the
   :class:`_schema.Table`
   refers to are matched to the classes to which they will be
   mapped, if any.

4. If mapped classes for both sides are located, a many-to-many bi-directional
   :func:`_orm.relationship` / :func:`.backref`
   pair is created between the two
   classes.

5. The override logic for many-to-many works the same as that of one-to-many/
   many-to-one; the :func:`.generate_relationship` function is called upon
   to generate the structures and existing attributes will be maintained.

Relationships with Inheritance
------------------------------

:mod:`.sqlalchemy.ext.automap` will not generate any relationships between
two classes that are in an inheritance relationship.   That is, with two
classes given as follows::

    class Employee(Base):
        __tablename__ = 'employee'
        id = Column(Integer, primary_key=True)
        type = Column(String(50))
        __mapper_args__ = {
             'polymorphic_identity':'employee', 'polymorphic_on': type
        }

    class Engineer(Employee):
        __tablename__ = 'engineer'
        id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
        __mapper_args__ = {
            'polymorphic_identity':'engineer',
        }

The foreign key from ``Engineer`` to ``Employee`` is used not for a
relationship, but to establish joined inheritance between the two classes.

Note that this means automap will not generate *any* relationships
for foreign keys that link from a subclass to a superclass.  If a mapping
has actual relationships from subclass to superclass as well, those
need to be explicit.  Below, as we have two separate foreign keys
from ``Engineer`` to ``Employee``, we need to set up both the relationship
we want as well as the ``inherit_condition``, as these are not things
SQLAlchemy can guess::

    class Employee(Base):
        __tablename__ = 'employee'
        id = Column(Integer, primary_key=True)
        type = Column(String(50))

        __mapper_args__ = {
            'polymorphic_identity':'employee', 'polymorphic_on':type
        }

    class Engineer(Employee):
        __tablename__ = 'engineer'
        id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
        favorite_employee_id = Column(Integer, ForeignKey('employee.id'))

        favorite_employee = relationship(Employee,
                                         foreign_keys=favorite_employee_id)

        __mapper_args__ = {
            'polymorphic_identity':'engineer',
            'inherit_condition': id == Employee.id
        }

Handling Simple Naming Conflicts
--------------------------------

In the case of naming conflicts during mapping, override any of
:func:`.classname_for_table`, :func:`.name_for_scalar_relationship`,
and :func:`.name_for_collection_relationship` as needed.  For example, if
automap is attempting to name a many-to-one relationship the same as an
existing column, an alternate convention can be conditionally selected.  Given
a schema:

.. sourcecode:: sql

    CREATE TABLE table_a (
        id INTEGER PRIMARY KEY
    );

    CREATE TABLE table_b (
        id INTEGER PRIMARY KEY,
        table_a INTEGER,
        FOREIGN KEY(table_a) REFERENCES table_a(id)
    );

The above schema will first automap the ``table_a`` table as a class named
``table_a``; it will then automap a relationship onto the class for ``table_b``
with the same name as this related class, e.g. ``table_a``.  This
relationship name conflicts with the mapping column ``table_b.table_a``,
and will emit an error on mapping.

We can resolve this conflict by using an underscore as follows::

    def name_for_scalar_relationship(base, local_cls, referred_cls, constraint):
        name = referred_cls.__name__.lower()
        local_table = local_cls.__table__
        if name in local_table.columns:
            newname = name + "_"
            warnings.warn(
                "Already detected name %s present.  using %s" %
                (name, newname))
            return newname
        return name


    Base.prepare(engine, reflect=True,
        name_for_scalar_relationship=name_for_scalar_relationship)

Alternatively, we can change the name on the column side.   The columns
that are mapped can be modified using the technique described at
:ref:`mapper_column_distinct_names`, by assigning the column explicitly
to a new name::

    Base = automap_base()

    class TableB(Base):
        __tablename__ = 'table_b'
        _table_a = Column('table_a', ForeignKey('table_a.id'))

    Base.prepare(engine, reflect=True)


Using Automap with Explicit Declarations
========================================

As noted previously, automap has no dependency on reflection, and can make
use of any collection of :class:`_schema.Table` objects within a
:class:`_schema.MetaData`
collection.  From this, it follows that automap can also be used
generate missing relationships given an otherwise complete model that fully
defines table metadata::

    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy import Column, Integer, String, ForeignKey

    Base = automap_base()

    class User(Base):
        __tablename__ = 'user'

        id = Column(Integer, primary_key=True)
        name = Column(String)

    class Address(Base):
        __tablename__ = 'address'

        id = Column(Integer, primary_key=True)
        email = Column(String)
        user_id = Column(ForeignKey('user.id'))

    # produce relationships
    Base.prepare()

    # mapping is complete, with "address_collection" and
    # "user" relationships
    a1 = Address(email='u1')
    a2 = Address(email='u2')
    u1 = User(address_collection=[a1, a2])
    assert a1.user is u1

Above, given mostly complete ``User`` and ``Address`` mappings, the
:class:`_schema.ForeignKey` which we defined on ``Address.user_id`` allowed a
bidirectional relationship pair ``Address.user`` and
``User.address_collection`` to be generated on the mapped classes.

Note that when subclassing :class:`.AutomapBase`,
the :meth:`.AutomapBase.prepare` method is required; if not called, the classes
we've declared are in an un-mapped state.


.. _automap_intercepting_columns:

Intercepting Column Definitions
===============================

The :class:`_schema.MetaData` and :class:`_schema.Table` objects support an
event hook :meth:`_events.DDLEvents.column_reflect` that may be used to intercept
the information reflected about a database column before the :class:`_schema.Column`
object is constructed.   For example if we wanted to map columns using a
naming convention such as ``"attr_<columnname>"``, the event could
be applied as::

    @event.listens_for(Base.metadata, "column_reflect")
    def column_reflect(inspector, table, column_info):
        # set column.key = "attr_<lower_case_name>"
        column_info['key'] = "attr_%s" % column_info['name'].lower()

    # run reflection
    Base.prepare(engine, reflect=True)

.. versionadded:: 1.4.0b2 the :meth:`_events.DDLEvents.column_reflect` event
   may be applied to a :class:`_schema.MetaData` object.

.. seealso::

      :meth:`_events.DDLEvents.column_reflect`

      :ref:`mapper_automated_reflection_schemes` - in the ORM mapping documentation


"""  # noqa
from .declarative import declarative_base as _declarative_base
from .. import util
from ..orm import backref
from ..orm import exc as orm_exc
from ..orm import interfaces
from ..orm import relationship
from ..orm.decl_base import _DeferredMapperConfig
from ..orm.mapper import _CONFIGURE_MUTEX
from ..schema import ForeignKeyConstraint
from ..sql import and_


def classname_for_table(base, tablename, table):
    """Return the class name that should be used, given the name
    of a table.

    The default implementation is::

        return str(tablename)

    Alternate implementations can be specified using the
    :paramref:`.AutomapBase.prepare.classname_for_table`
    parameter.

    :param base: the :class:`.AutomapBase` class doing the prepare.

    :param tablename: string name of the :class:`_schema.Table`.

    :param table: the :class:`_schema.Table` object itself.

    :return: a string class name.

     .. note::

        In Python 2, the string used for the class name **must** be a
        non-Unicode object, e.g. a ``str()`` object.  The ``.name`` attribute
        of :class:`_schema.Table` is typically a Python unicode subclass,
        so the
        ``str()`` function should be applied to this name, after accounting for
        any non-ASCII characters.

    """
    return str(tablename)


def name_for_scalar_relationship(base, local_cls, referred_cls, constraint):
    """Return the attribute name that should be used to refer from one
    class to another, for a scalar object reference.

    The default implementation is::

        return referred_cls.__name__.lower()

    Alternate implementations can be specified using the
    :paramref:`.AutomapBase.prepare.name_for_scalar_relationship`
    parameter.

    :param base: the :class:`.AutomapBase` class doing the prepare.

    :param local_cls: the class to be mapped on the local side.

    :param referred_cls: the class to be mapped on the referring side.

    :param constraint: the :class:`_schema.ForeignKeyConstraint` that is being
     inspected to produce this relationship.

    """
    return referred_cls.__name__.lower()


def name_for_collection_relationship(
    base, local_cls, referred_cls, constraint
):
    """Return the attribute name that should be used to refer from one
    class to another, for a collection reference.

    The default implementation is::

        return referred_cls.__name__.lower() + "_collection"

    Alternate implementations
    can be specified using the
    :paramref:`.AutomapBase.prepare.name_for_collection_relationship`
    parameter.

    :param base: the :class:`.AutomapBase` class doing the prepare.

    :param local_cls: the class to be mapped on the local side.

    :param referred_cls: the class to be mapped on the referring side.

    :param constraint: the :class:`_schema.ForeignKeyConstraint` that is being
     inspected to produce this relationship.

    """
    return referred_cls.__name__.lower() + "_collection"


def generate_relationship(
    base, direction, return_fn, attrname, local_cls, referred_cls, **kw
):
    r"""Generate a :func:`_orm.relationship` or :func:`.backref`
    on behalf of two
    mapped classes.

    An alternate implementation of this function can be specified using the
    :paramref:`.AutomapBase.prepare.generate_relationship` parameter.

    The default implementation of this function is as follows::

        if return_fn is backref:
            return return_fn(attrname, **kw)
        elif return_fn is relationship:
            return return_fn(referred_cls, **kw)
        else:
            raise TypeError("Unknown relationship function: %s" % return_fn)

    :param base: the :class:`.AutomapBase` class doing the prepare.

    :param direction: indicate the "direction" of the relationship; this will
     be one of :data:`.ONETOMANY`, :data:`.MANYTOONE`, :data:`.MANYTOMANY`.

    :param return_fn: the function that is used by default to create the
     relationship.  This will be either :func:`_orm.relationship` or
     :func:`.backref`.  The :func:`.backref` function's result will be used to
     produce a new :func:`_orm.relationship` in a second step,
     so it is critical
     that user-defined implementations correctly differentiate between the two
     functions, if a custom relationship function is being used.

    :param attrname: the attribute name to which this relationship is being
     assigned. If the value of :paramref:`.generate_relationship.return_fn` is
     the :func:`.backref` function, then this name is the name that is being
     assigned to the backref.

    :param local_cls: the "local" class to which this relationship or backref
     will be locally present.

    :param referred_cls: the "referred" class to which the relationship or
     backref refers to.

    :param \**kw: all additional keyword arguments are passed along to the
     function.

    :return: a :func:`_orm.relationship` or :func:`.backref` construct,
     as dictated
     by the :paramref:`.generate_relationship.return_fn` parameter.

    """
    if return_fn is backref:
        return return_fn(attrname, **kw)
    elif return_fn is relationship:
        return return_fn(referred_cls, **kw)
    else:
        raise TypeError("Unknown relationship function: %s" % return_fn)


class AutomapBase(object):
    """Base class for an "automap" schema.

    The :class:`.AutomapBase` class can be compared to the "declarative base"
    class that is produced by the :func:`.declarative.declarative_base`
    function.  In practice, the :class:`.AutomapBase` class is always used
    as a mixin along with an actual declarative base.

    A new subclassable :class:`.AutomapBase` is typically instantiated
    using the :func:`.automap_base` function.

    .. seealso::

        :ref:`automap_toplevel`

    """

    __abstract__ = True

    classes = None
    """An instance of :class:`.util.Properties` containing classes.

    This object behaves much like the ``.c`` collection on a table.  Classes
    are present under the name they were given, e.g.::

        Base = automap_base()
        Base.prepare(engine=some_engine, reflect=True)

        User, Address = Base.classes.User, Base.classes.Address

    """

    @classmethod
    @util.deprecated_params(
        engine=(
            "2.0",
            "The :paramref:`_automap.AutomapBase.prepare.engine` parameter "
            "is deprecated and will be removed in a future release.  "
            "Please use the "
            ":paramref:`_automap.AutomapBase.prepare.autoload_with` "
            "parameter.",
        ),
        reflect=(
            "2.0",
            "The :paramref:`_automap.AutomapBase.prepare.reflect` "
            "parameter is deprecated and will be removed in a future "
            "release.  Reflection is enabled when "
            ":paramref:`_automap.AutomapBase.prepare.autoload_with` "
            "is passed.",
        ),
    )
    def prepare(
        cls,
        autoload_with=None,
        engine=None,
        reflect=False,
        schema=None,
        classname_for_table=None,
        collection_class=None,
        name_for_scalar_relationship=None,
        name_for_collection_relationship=None,
        generate_relationship=None,
        reflection_options=util.EMPTY_DICT,
    ):
        """Extract mapped classes and relationships from the
        :class:`_schema.MetaData` and
        perform mappings.

        :param engine: an :class:`_engine.Engine` or
         :class:`_engine.Connection` with which
         to perform schema reflection, if specified.
         If the :paramref:`.AutomapBase.prepare.reflect` argument is False,
         this object is not used.

        :param reflect: if True, the :meth:`_schema.MetaData.reflect`
         method is called
         on the :class:`_schema.MetaData` associated with this
         :class:`.AutomapBase`.
         The :class:`_engine.Engine` passed via
         :paramref:`.AutomapBase.prepare.engine` will be used to perform the
         reflection if present; else, the :class:`_schema.MetaData`
         should already be
         bound to some engine else the operation will fail.

        :param classname_for_table: callable function which will be used to
         produce new class names, given a table name.  Defaults to
         :func:`.classname_for_table`.

        :param name_for_scalar_relationship: callable function which will be
         used to produce relationship names for scalar relationships.  Defaults
         to :func:`.name_for_scalar_relationship`.

        :param name_for_collection_relationship: callable function which will
         be used to produce relationship names for collection-oriented
         relationships.  Defaults to :func:`.name_for_collection_relationship`.

        :param generate_relationship: callable function which will be used to
         actually generate :func:`_orm.relationship` and :func:`.backref`
         constructs.  Defaults to :func:`.generate_relationship`.

        :param collection_class: the Python collection class that will be used
         when a new :func:`_orm.relationship`
         object is created that represents a
         collection.  Defaults to ``list``.

        :param schema: When present in conjunction with the
         :paramref:`.AutomapBase.prepare.reflect` flag, is passed to
         :meth:`_schema.MetaData.reflect`
         to indicate the primary schema where tables
         should be reflected from.  When omitted, the default schema in use
         by the database connection is used.

         .. versionadded:: 1.1

        :param reflection_options: When present, this dictionary of options
         will be passed to :meth:`_schema.MetaData.reflect`
         to supply general reflection-specific options like ``only`` and/or
         dialect-specific options like ``oracle_resolve_synonyms``.

         .. versionadded:: 1.4

        """
        glbls = globals()
        if classname_for_table is None:
            classname_for_table = glbls["classname_for_table"]
        if name_for_scalar_relationship is None:
            name_for_scalar_relationship = glbls[
                "name_for_scalar_relationship"
            ]
        if name_for_collection_relationship is None:
            name_for_collection_relationship = glbls[
                "name_for_collection_relationship"
            ]
        if generate_relationship is None:
            generate_relationship = glbls["generate_relationship"]
        if collection_class is None:
            collection_class = list

        if autoload_with:
            reflect = True

        if engine:
            autoload_with = engine

        if reflect:
            opts = dict(
                schema=schema,
                extend_existing=True,
                autoload_replace=False,
            )
            if reflection_options:
                opts.update(reflection_options)
            cls.metadata.reflect(autoload_with, **opts)

        with _CONFIGURE_MUTEX:
            table_to_map_config = dict(
                (m.local_table, m)
                for m in _DeferredMapperConfig.classes_for_base(
                    cls, sort=False
                )
            )

            many_to_many = []

            for table in cls.metadata.tables.values():
                lcl_m2m, rem_m2m, m2m_const = _is_many_to_many(cls, table)
                if lcl_m2m is not None:
                    many_to_many.append((lcl_m2m, rem_m2m, m2m_const, table))
                elif not table.primary_key:
                    continue
                elif table not in table_to_map_config:
                    mapped_cls = type(
                        classname_for_table(cls, table.name, table),
                        (cls,),
                        {"__table__": table},
                    )
                    map_config = _DeferredMapperConfig.config_for_cls(
                        mapped_cls
                    )
                    cls.classes[map_config.cls.__name__] = mapped_cls
                    table_to_map_config[table] = map_config

            for map_config in table_to_map_config.values():
                _relationships_for_fks(
                    cls,
                    map_config,
                    table_to_map_config,
                    collection_class,
                    name_for_scalar_relationship,
                    name_for_collection_relationship,
                    generate_relationship,
                )

            for lcl_m2m, rem_m2m, m2m_const, table in many_to_many:
                _m2m_relationship(
                    cls,
                    lcl_m2m,
                    rem_m2m,
                    m2m_const,
                    table,
                    table_to_map_config,
                    collection_class,
                    name_for_scalar_relationship,
                    name_for_collection_relationship,
                    generate_relationship,
                )

            for map_config in _DeferredMapperConfig.classes_for_base(cls):
                map_config.map()

    _sa_decl_prepare = True
    """Indicate that the mapping of classes should be deferred.

    The presence of this attribute name indicates to declarative
    that the call to mapper() should not occur immediately; instead,
    information about the table and attributes to be mapped are gathered
    into an internal structure called _DeferredMapperConfig.  These
    objects can be collected later using classes_for_base(), additional
    mapping decisions can be made, and then the map() method will actually
    apply the mapping.

    The only real reason this deferral of the whole
    thing is needed is to support primary key columns that aren't reflected
    yet when the class is declared; everything else can theoretically be
    added to the mapper later.  However, the _DeferredMapperConfig is a
    nice interface in any case which exists at that not usually exposed point
    at which declarative has the class and the Table but hasn't called
    mapper() yet.

    """

    @classmethod
    def _sa_raise_deferred_config(cls):
        raise orm_exc.UnmappedClassError(
            cls,
            msg="Class %s is a subclass of AutomapBase.  "
            "Mappings are not produced until the .prepare() "
            "method is called on the class hierarchy."
            % orm_exc._safe_cls_name(cls),
        )


def automap_base(declarative_base=None, **kw):
    r"""Produce a declarative automap base.

    This function produces a new base class that is a product of the
    :class:`.AutomapBase` class as well a declarative base produced by
    :func:`.declarative.declarative_base`.

    All parameters other than ``declarative_base`` are keyword arguments
    that are passed directly to the :func:`.declarative.declarative_base`
    function.

    :param declarative_base: an existing class produced by
     :func:`.declarative.declarative_base`.  When this is passed, the function
     no longer invokes :func:`.declarative.declarative_base` itself, and all
     other keyword arguments are ignored.

    :param \**kw: keyword arguments are passed along to
     :func:`.declarative.declarative_base`.

    """
    if declarative_base is None:
        Base = _declarative_base(**kw)
    else:
        Base = declarative_base

    return type(
        Base.__name__,
        (AutomapBase, Base),
        {"__abstract__": True, "classes": util.Properties({})},
    )


def _is_many_to_many(automap_base, table):
    fk_constraints = [
        const
        for const in table.constraints
        if isinstance(const, ForeignKeyConstraint)
    ]
    if len(fk_constraints) != 2:
        return None, None, None

    cols = sum(
        [
            [fk.parent for fk in fk_constraint.elements]
            for fk_constraint in fk_constraints
        ],
        [],
    )

    if set(cols) != set(table.c):
        return None, None, None

    return (
        fk_constraints[0].elements[0].column.table,
        fk_constraints[1].elements[0].column.table,
        fk_constraints,
    )


def _relationships_for_fks(
    automap_base,
    map_config,
    table_to_map_config,
    collection_class,
    name_for_scalar_relationship,
    name_for_collection_relationship,
    generate_relationship,
):
    local_table = map_config.local_table
    local_cls = map_config.cls  # derived from a weakref, may be None

    if local_table is None or local_cls is None:
        return
    for constraint in local_table.constraints:
        if isinstance(constraint, ForeignKeyConstraint):
            fks = constraint.elements
            referred_table = fks[0].column.table
            referred_cfg = table_to_map_config.get(referred_table, None)
            if referred_cfg is None:
                continue
            referred_cls = referred_cfg.cls

            if local_cls is not referred_cls and issubclass(
                local_cls, referred_cls
            ):
                continue

            relationship_name = name_for_scalar_relationship(
                automap_base, local_cls, referred_cls, constraint
            )
            backref_name = name_for_collection_relationship(
                automap_base, referred_cls, local_cls, constraint
            )

            o2m_kws = {}
            nullable = False not in {fk.parent.nullable for fk in fks}
            if not nullable:
                o2m_kws["cascade"] = "all, delete-orphan"

                if (
                    constraint.ondelete
                    and constraint.ondelete.lower() == "cascade"
                ):
                    o2m_kws["passive_deletes"] = True
            else:
                if (
                    constraint.ondelete
                    and constraint.ondelete.lower() == "set null"
                ):
                    o2m_kws["passive_deletes"] = True

            create_backref = backref_name not in referred_cfg.properties

            if relationship_name not in map_config.properties:
                if create_backref:
                    backref_obj = generate_relationship(
                        automap_base,
                        interfaces.ONETOMANY,
                        backref,
                        backref_name,
                        referred_cls,
                        local_cls,
                        collection_class=collection_class,
                        **o2m_kws
                    )
                else:
                    backref_obj = None
                rel = generate_relationship(
                    automap_base,
                    interfaces.MANYTOONE,
                    relationship,
                    relationship_name,
                    local_cls,
                    referred_cls,
                    foreign_keys=[fk.parent for fk in constraint.elements],
                    backref=backref_obj,
                    remote_side=[fk.column for fk in constraint.elements],
                )
                if rel is not None:
                    map_config.properties[relationship_name] = rel
                    if not create_backref:
                        referred_cfg.properties[
                            backref_name
                        ].back_populates = relationship_name
            elif create_backref:
                rel = generate_relationship(
                    automap_base,
                    interfaces.ONETOMANY,
                    relationship,
                    backref_name,
                    referred_cls,
                    local_cls,
                    foreign_keys=[fk.parent for fk in constraint.elements],
                    back_populates=relationship_name,
                    collection_class=collection_class,
                    **o2m_kws
                )
                if rel is not None:
                    referred_cfg.properties[backref_name] = rel
                    map_config.properties[
                        relationship_name
                    ].back_populates = backref_name


def _m2m_relationship(
    automap_base,
    lcl_m2m,
    rem_m2m,
    m2m_const,
    table,
    table_to_map_config,
    collection_class,
    name_for_scalar_relationship,
    name_for_collection_relationship,
    generate_relationship,
):

    map_config = table_to_map_config.get(lcl_m2m, None)
    referred_cfg = table_to_map_config.get(rem_m2m, None)
    if map_config is None or referred_cfg is None:
        return

    local_cls = map_config.cls
    referred_cls = referred_cfg.cls

    relationship_name = name_for_collection_relationship(
        automap_base, local_cls, referred_cls, m2m_const[0]
    )
    backref_name = name_for_collection_relationship(
        automap_base, referred_cls, local_cls, m2m_const[1]
    )

    create_backref = backref_name not in referred_cfg.properties

    if relationship_name not in map_config.properties:
        if create_backref:
            backref_obj = generate_relationship(
                automap_base,
                interfaces.MANYTOMANY,
                backref,
                backref_name,
                referred_cls,
                local_cls,
                collection_class=collection_class,
            )
        else:
            backref_obj = None
        rel = generate_relationship(
            automap_base,
            interfaces.MANYTOMANY,
            relationship,
            relationship_name,
            local_cls,
            referred_cls,
            secondary=table,
            primaryjoin=and_(
                fk.column == fk.parent for fk in m2m_const[0].elements
            ),
            secondaryjoin=and_(
                fk.column == fk.parent for fk in m2m_const[1].elements
            ),
            backref=backref_obj,
            collection_class=collection_class,
        )
        if rel is not None:
            map_config.properties[relationship_name] = rel

            if not create_backref:
                referred_cfg.properties[
                    backref_name
                ].back_populates = relationship_name
    elif create_backref:
        rel = generate_relationship(
            automap_base,
            interfaces.MANYTOMANY,
            relationship,
            backref_name,
            referred_cls,
            local_cls,
            secondary=table,
            primaryjoin=and_(
                fk.column == fk.parent for fk in m2m_const[1].elements
            ),
            secondaryjoin=and_(
                fk.column == fk.parent for fk in m2m_const[0].elements
            ),
            back_populates=relationship_name,
            collection_class=collection_class,
        )
        if rel is not None:
            referred_cfg.properties[backref_name] = rel
            map_config.properties[
                relationship_name
            ].back_populates = backref_name
