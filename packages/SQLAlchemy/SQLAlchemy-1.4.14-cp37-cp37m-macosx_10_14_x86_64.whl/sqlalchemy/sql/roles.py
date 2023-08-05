# sql/roles.py
# Copyright (C) 2005-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from .. import util


class SQLRole(object):
    """Define a "role" within a SQL statement structure.

    Classes within SQL Core participate within SQLRole hierarchies in order
    to more accurately indicate where they may be used within SQL statements
    of all types.

    .. versionadded:: 1.4

    """

    allows_lambda = False
    uses_inspection = False


class UsesInspection(object):
    _post_inspect = None
    uses_inspection = True


class AllowsLambdaRole(object):
    allows_lambda = True


class HasCacheKeyRole(SQLRole):
    _role_name = "Cacheable Core or ORM object"


class LiteralValueRole(SQLRole):
    _role_name = "Literal Python value"


class ColumnArgumentRole(SQLRole):
    _role_name = "Column expression"


class ColumnArgumentOrKeyRole(ColumnArgumentRole):
    _role_name = "Column expression or string key"


class StrAsPlainColumnRole(ColumnArgumentRole):
    _role_name = "Column expression or string key"


class ColumnListRole(SQLRole):
    """Elements suitable for forming comma separated lists of expressions."""


class TruncatedLabelRole(SQLRole):
    _role_name = "String SQL identifier"


class ColumnsClauseRole(AllowsLambdaRole, UsesInspection, ColumnListRole):
    _role_name = "Column expression or FROM clause"

    @property
    def _select_iterable(self):
        raise NotImplementedError()


class LimitOffsetRole(SQLRole):
    _role_name = "LIMIT / OFFSET expression"


class ByOfRole(ColumnListRole):
    _role_name = "GROUP BY / OF / etc. expression"


class GroupByRole(AllowsLambdaRole, UsesInspection, ByOfRole):
    # note there's a special case right now where you can pass a whole
    # ORM entity to group_by() and it splits out.   we may not want to keep
    # this around

    _role_name = "GROUP BY expression"


class OrderByRole(AllowsLambdaRole, ByOfRole):
    _role_name = "ORDER BY expression"


class StructuralRole(SQLRole):
    pass


class StatementOptionRole(StructuralRole):
    _role_name = "statement sub-expression element"


class OnClauseRole(AllowsLambdaRole, StructuralRole):
    _role_name = "SQL expression for ON clause"


class WhereHavingRole(OnClauseRole):
    _role_name = "SQL expression for WHERE/HAVING role"


class ExpressionElementRole(SQLRole):
    _role_name = "SQL expression element"


class ConstExprRole(ExpressionElementRole):
    _role_name = "Constant True/False/None expression"


class LabeledColumnExprRole(ExpressionElementRole):
    pass


class BinaryElementRole(ExpressionElementRole):
    _role_name = "SQL expression element or literal value"


class InElementRole(SQLRole):
    _role_name = (
        "IN expression list, SELECT construct, or bound parameter object"
    )


class JoinTargetRole(AllowsLambdaRole, UsesInspection, StructuralRole):
    _role_name = (
        "Join target, typically a FROM expression, or ORM "
        "relationship attribute"
    )


class FromClauseRole(ColumnsClauseRole, JoinTargetRole):
    _role_name = "FROM expression, such as a Table or alias() object"

    _is_subquery = False

    @property
    def _hide_froms(self):
        raise NotImplementedError()


class StrictFromClauseRole(FromClauseRole):
    # does not allow text() or select() objects
    pass


class AnonymizedFromClauseRole(StrictFromClauseRole):
    # calls .alias() as a post processor

    def _anonymous_fromclause(self, name=None, flat=False):
        raise NotImplementedError()


class ReturnsRowsRole(SQLRole):
    _role_name = (
        "Row returning expression such as a SELECT, a FROM clause, or an "
        "INSERT/UPDATE/DELETE with RETURNING"
    )


class StatementRole(SQLRole):
    _role_name = "Executable SQL or text() construct"

    _propagate_attrs = util.immutabledict()


class SelectStatementRole(StatementRole, ReturnsRowsRole):
    _role_name = "SELECT construct or equivalent text() construct"

    def subquery(self):
        raise NotImplementedError(
            "All SelectStatementRole objects should implement a "
            ".subquery() method."
        )


class HasCTERole(ReturnsRowsRole):
    pass


class CompoundElementRole(AllowsLambdaRole, SQLRole):
    """SELECT statements inside a CompoundSelect, e.g. UNION, EXTRACT, etc."""

    _role_name = (
        "SELECT construct for inclusion in a UNION or other set construct"
    )


# TODO: are we using this?
class DMLRole(StatementRole):
    pass


class DMLTableRole(FromClauseRole):
    _role_name = "subject table for an INSERT, UPDATE or DELETE"


class DMLColumnRole(SQLRole):
    _role_name = "SET/VALUES column expression or string key"


class DMLSelectRole(SQLRole):
    """A SELECT statement embedded in DML, typically INSERT from SELECT """

    _role_name = "SELECT statement or equivalent textual object"


class DDLRole(StatementRole):
    pass


class DDLExpressionRole(StructuralRole):
    _role_name = "SQL expression element for DDL constraint"


class DDLConstraintColumnRole(SQLRole):
    _role_name = "String column name or column expression for DDL constraint"


class DDLReferredColumnRole(DDLConstraintColumnRole):
    _role_name = (
        "String column name or Column object for DDL foreign key constraint"
    )
