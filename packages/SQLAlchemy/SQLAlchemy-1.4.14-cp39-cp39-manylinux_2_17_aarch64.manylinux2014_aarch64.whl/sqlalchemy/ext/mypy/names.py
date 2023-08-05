# ext/mypy/names.py
# Copyright (C) 2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

from mypy.nodes import ClassDef
from mypy.nodes import Expression
from mypy.nodes import FuncDef
from mypy.nodes import MemberExpr
from mypy.nodes import NameExpr
from mypy.nodes import SymbolNode
from mypy.nodes import TypeAlias
from mypy.nodes import TypeInfo
from mypy.plugin import SemanticAnalyzerPluginInterface
from mypy.types import CallableType
from mypy.types import get_proper_type
from mypy.types import Instance
from mypy.types import UnboundType

from ... import util

COLUMN: int = util.symbol("COLUMN")  # type: ignore
RELATIONSHIP: int = util.symbol("RELATIONSHIP")  # type: ignore
REGISTRY: int = util.symbol("REGISTRY")  # type: ignore
COLUMN_PROPERTY: int = util.symbol("COLUMN_PROPERTY")  # type: ignore
TYPEENGINE: int = util.symbol("TYPEENGNE")  # type: ignore
MAPPED: int = util.symbol("MAPPED")  # type: ignore
DECLARATIVE_BASE: int = util.symbol("DECLARATIVE_BASE")  # type: ignore
DECLARATIVE_META: int = util.symbol("DECLARATIVE_META")  # type: ignore
MAPPED_DECORATOR: int = util.symbol("MAPPED_DECORATOR")  # type: ignore
COLUMN_PROPERTY: int = util.symbol("COLUMN_PROPERTY")  # type: ignore
SYNONYM_PROPERTY: int = util.symbol("SYNONYM_PROPERTY")  # type: ignore
COMPOSITE_PROPERTY: int = util.symbol("COMPOSITE_PROPERTY")  # type: ignore
DECLARED_ATTR: int = util.symbol("DECLARED_ATTR")  # type: ignore
MAPPER_PROPERTY: int = util.symbol("MAPPER_PROPERTY")  # type: ignore
AS_DECLARATIVE: int = util.symbol("AS_DECLARATIVE")  # type: ignore
AS_DECLARATIVE_BASE: int = util.symbol("AS_DECLARATIVE_BASE")  # type: ignore
DECLARATIVE_MIXIN: int = util.symbol("DECLARATIVE_MIXIN")  # type: ignore

_lookup: Dict[str, Tuple[int, Set[str]]] = {
    "Column": (
        COLUMN,
        {
            "sqlalchemy.sql.schema.Column",
            "sqlalchemy.sql.Column",
        },
    ),
    "RelationshipProperty": (
        RELATIONSHIP,
        {
            "sqlalchemy.orm.relationships.RelationshipProperty",
            "sqlalchemy.orm.RelationshipProperty",
        },
    ),
    "registry": (
        REGISTRY,
        {
            "sqlalchemy.orm.decl_api.registry",
            "sqlalchemy.orm.registry",
        },
    ),
    "ColumnProperty": (
        COLUMN_PROPERTY,
        {
            "sqlalchemy.orm.properties.ColumnProperty",
            "sqlalchemy.orm.ColumnProperty",
        },
    ),
    "SynonymProperty": (
        SYNONYM_PROPERTY,
        {
            "sqlalchemy.orm.descriptor_props.SynonymProperty",
            "sqlalchemy.orm.SynonymProperty",
        },
    ),
    "CompositeProperty": (
        COMPOSITE_PROPERTY,
        {
            "sqlalchemy.orm.descriptor_props.CompositeProperty",
            "sqlalchemy.orm.CompositeProperty",
        },
    ),
    "MapperProperty": (
        MAPPER_PROPERTY,
        {
            "sqlalchemy.orm.interfaces.MapperProperty",
            "sqlalchemy.orm.MapperProperty",
        },
    ),
    "TypeEngine": (TYPEENGINE, {"sqlalchemy.sql.type_api.TypeEngine"}),
    "Mapped": (MAPPED, {"sqlalchemy.orm.attributes.Mapped"}),
    "declarative_base": (
        DECLARATIVE_BASE,
        {
            "sqlalchemy.ext.declarative.declarative_base",
            "sqlalchemy.orm.declarative_base",
            "sqlalchemy.orm.decl_api.declarative_base",
        },
    ),
    "DeclarativeMeta": (
        DECLARATIVE_META,
        {
            "sqlalchemy.ext.declarative.DeclarativeMeta",
            "sqlalchemy.orm.DeclarativeMeta",
            "sqlalchemy.orm.decl_api.DeclarativeMeta",
        },
    ),
    "mapped": (
        MAPPED_DECORATOR,
        {
            "sqlalchemy.orm.decl_api.registry.mapped",
            "sqlalchemy.orm.registry.mapped",
        },
    ),
    "as_declarative": (
        AS_DECLARATIVE,
        {
            "sqlalchemy.ext.declarative.as_declarative",
            "sqlalchemy.orm.decl_api.as_declarative",
            "sqlalchemy.orm.as_declarative",
        },
    ),
    "as_declarative_base": (
        AS_DECLARATIVE_BASE,
        {
            "sqlalchemy.orm.decl_api.registry.as_declarative_base",
            "sqlalchemy.orm.registry.as_declarative_base",
        },
    ),
    "declared_attr": (
        DECLARED_ATTR,
        {
            "sqlalchemy.orm.decl_api.declared_attr",
            "sqlalchemy.orm.declared_attr",
        },
    ),
    "declarative_mixin": (
        DECLARATIVE_MIXIN,
        {
            "sqlalchemy.orm.decl_api.declarative_mixin",
            "sqlalchemy.orm.declarative_mixin",
        },
    ),
}


def _has_base_type_id(info: TypeInfo, type_id: int) -> bool:
    for mr in info.mro:
        check_type_id, fullnames = _lookup.get(mr.name, (None, None))
        if check_type_id == type_id:
            break
    else:
        return False

    if fullnames is None:
        return False

    return mr.fullname in fullnames


def _mro_has_id(mro: List[TypeInfo], type_id: int) -> bool:
    for mr in mro:
        check_type_id, fullnames = _lookup.get(mr.name, (None, None))
        if check_type_id == type_id:
            break
    else:
        return False

    if fullnames is None:
        return False

    return mr.fullname in fullnames


def _type_id_for_unbound_type(
    type_: UnboundType, cls: ClassDef, api: SemanticAnalyzerPluginInterface
) -> Optional[int]:
    type_id = None

    sym = api.lookup_qualified(type_.name, type_)
    if sym is not None:
        if isinstance(sym.node, TypeAlias):
            target_type = get_proper_type(sym.node.target)
            if isinstance(target_type, Instance):
                type_id = _type_id_for_named_node(target_type.type)
        elif isinstance(sym.node, TypeInfo):
            type_id = _type_id_for_named_node(sym.node)

    return type_id


def _type_id_for_callee(callee: Expression) -> Optional[int]:
    if isinstance(callee, (MemberExpr, NameExpr)):
        if isinstance(callee.node, FuncDef):
            return _type_id_for_funcdef(callee.node)
        elif isinstance(callee.node, TypeAlias):
            target_type = get_proper_type(callee.node.target)
            if isinstance(target_type, Instance):
                type_id = _type_id_for_fullname(target_type.type.fullname)
        elif isinstance(callee.node, TypeInfo):
            type_id = _type_id_for_named_node(callee)
        else:
            type_id = None
    return type_id


def _type_id_for_funcdef(node: FuncDef) -> Optional[int]:
    if node.type and isinstance(node.type, CallableType):
        ret_type = get_proper_type(node.type.ret_type)

        if isinstance(ret_type, Instance):
            return _type_id_for_fullname(ret_type.type.fullname)

    return None


def _type_id_for_named_node(
    node: Union[NameExpr, MemberExpr, SymbolNode]
) -> Optional[int]:
    type_id, fullnames = _lookup.get(node.name, (None, None))

    if type_id is None or fullnames is None:
        return None
    elif node.fullname in fullnames:
        return type_id
    else:
        return None


def _type_id_for_fullname(fullname: str) -> Optional[int]:
    tokens = fullname.split(".")
    immediate = tokens[-1]

    type_id, fullnames = _lookup.get(immediate, (None, None))

    if type_id is None or fullnames is None:
        return None
    elif fullname in fullnames:
        return type_id
    else:
        return None
