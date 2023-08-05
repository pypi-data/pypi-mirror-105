# orm/dependency.py
# Copyright (C) 2005-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""Relationship dependencies.

"""

from . import attributes
from . import exc
from . import sync
from . import unitofwork
from . import util as mapperutil
from .interfaces import MANYTOMANY
from .interfaces import MANYTOONE
from .interfaces import ONETOMANY
from .. import exc as sa_exc
from .. import sql
from .. import util


class DependencyProcessor(object):
    def __init__(self, prop):
        self.prop = prop
        self.cascade = prop.cascade
        self.mapper = prop.mapper
        self.parent = prop.parent
        self.secondary = prop.secondary
        self.direction = prop.direction
        self.post_update = prop.post_update
        self.passive_deletes = prop.passive_deletes
        self.passive_updates = prop.passive_updates
        self.enable_typechecks = prop.enable_typechecks
        if self.passive_deletes:
            self._passive_delete_flag = attributes.PASSIVE_NO_INITIALIZE
        else:
            self._passive_delete_flag = attributes.PASSIVE_OFF
        if self.passive_updates:
            self._passive_update_flag = attributes.PASSIVE_NO_INITIALIZE
        else:
            self._passive_update_flag = attributes.PASSIVE_OFF

        self.sort_key = "%s_%s" % (self.parent._sort_key, prop.key)
        self.key = prop.key
        if not self.prop.synchronize_pairs:
            raise sa_exc.ArgumentError(
                "Can't build a DependencyProcessor for relationship %s. "
                "No target attributes to populate between parent and "
                "child are present" % self.prop
            )

    @classmethod
    def from_relationship(cls, prop):
        return _direction_to_processor[prop.direction](prop)

    def hasparent(self, state):
        """return True if the given object instance has a parent,
        according to the ``InstrumentedAttribute`` handled by this
        ``DependencyProcessor``.

        """
        return self.parent.class_manager.get_impl(self.key).hasparent(state)

    def per_property_preprocessors(self, uow):
        """establish actions and dependencies related to a flush.

        These actions will operate on all relevant states in
        the aggregate.

        """
        uow.register_preprocessor(self, True)

    def per_property_flush_actions(self, uow):
        after_save = unitofwork.ProcessAll(uow, self, False, True)
        before_delete = unitofwork.ProcessAll(uow, self, True, True)

        parent_saves = unitofwork.SaveUpdateAll(
            uow, self.parent.primary_base_mapper
        )
        child_saves = unitofwork.SaveUpdateAll(
            uow, self.mapper.primary_base_mapper
        )

        parent_deletes = unitofwork.DeleteAll(
            uow, self.parent.primary_base_mapper
        )
        child_deletes = unitofwork.DeleteAll(
            uow, self.mapper.primary_base_mapper
        )

        self.per_property_dependencies(
            uow,
            parent_saves,
            child_saves,
            parent_deletes,
            child_deletes,
            after_save,
            before_delete,
        )

    def per_state_flush_actions(self, uow, states, isdelete):
        """establish actions and dependencies related to a flush.

        These actions will operate on all relevant states
        individually.    This occurs only if there are cycles
        in the 'aggregated' version of events.

        """

        child_base_mapper = self.mapper.primary_base_mapper
        child_saves = unitofwork.SaveUpdateAll(uow, child_base_mapper)
        child_deletes = unitofwork.DeleteAll(uow, child_base_mapper)

        # locate and disable the aggregate processors
        # for this dependency

        if isdelete:
            before_delete = unitofwork.ProcessAll(uow, self, True, True)
            before_delete.disabled = True
        else:
            after_save = unitofwork.ProcessAll(uow, self, False, True)
            after_save.disabled = True

        # check if the "child" side is part of the cycle

        if child_saves not in uow.cycles:
            # based on the current dependencies we use, the saves/
            # deletes should always be in the 'cycles' collection
            # together.   if this changes, we will have to break up
            # this method a bit more.
            assert child_deletes not in uow.cycles

            # child side is not part of the cycle, so we will link per-state
            # actions to the aggregate "saves", "deletes" actions
            child_actions = [(child_saves, False), (child_deletes, True)]
            child_in_cycles = False
        else:
            child_in_cycles = True

        # check if the "parent" side is part of the cycle
        if not isdelete:
            parent_saves = unitofwork.SaveUpdateAll(
                uow, self.parent.base_mapper
            )
            parent_deletes = before_delete = None
            if parent_saves in uow.cycles:
                parent_in_cycles = True
        else:
            parent_deletes = unitofwork.DeleteAll(uow, self.parent.base_mapper)
            parent_saves = after_save = None
            if parent_deletes in uow.cycles:
                parent_in_cycles = True

        # now create actions /dependencies for each state.

        for state in states:
            # detect if there's anything changed or loaded
            # by a preprocessor on this state/attribute.   In the
            # case of deletes we may try to load missing items here as well.
            sum_ = state.manager[self.key].impl.get_all_pending(
                state,
                state.dict,
                self._passive_delete_flag
                if isdelete
                else attributes.PASSIVE_NO_INITIALIZE,
            )

            if not sum_:
                continue

            if isdelete:
                before_delete = unitofwork.ProcessState(uow, self, True, state)
                if parent_in_cycles:
                    parent_deletes = unitofwork.DeleteState(uow, state)
            else:
                after_save = unitofwork.ProcessState(uow, self, False, state)
                if parent_in_cycles:
                    parent_saves = unitofwork.SaveUpdateState(uow, state)

            if child_in_cycles:
                child_actions = []
                for child_state, child in sum_:
                    if child_state not in uow.states:
                        child_action = (None, None)
                    else:
                        (deleted, listonly) = uow.states[child_state]
                        if deleted:
                            child_action = (
                                unitofwork.DeleteState(uow, child_state),
                                True,
                            )
                        else:
                            child_action = (
                                unitofwork.SaveUpdateState(uow, child_state),
                                False,
                            )
                    child_actions.append(child_action)

            # establish dependencies between our possibly per-state
            # parent action and our possibly per-state child action.
            for child_action, childisdelete in child_actions:
                self.per_state_dependencies(
                    uow,
                    parent_saves,
                    parent_deletes,
                    child_action,
                    after_save,
                    before_delete,
                    isdelete,
                    childisdelete,
                )

    def presort_deletes(self, uowcommit, states):
        return False

    def presort_saves(self, uowcommit, states):
        return False

    def process_deletes(self, uowcommit, states):
        pass

    def process_saves(self, uowcommit, states):
        pass

    def prop_has_changes(self, uowcommit, states, isdelete):
        if not isdelete or self.passive_deletes:
            passive = attributes.PASSIVE_NO_INITIALIZE
        elif self.direction is MANYTOONE:
            # here, we were hoping to optimize having to fetch many-to-one
            # for history and ignore it, if there's no further cascades
            # to take place.  however there are too many less common conditions
            # that still take place and tests in test_relationships /
            # test_cascade etc. will still fail.
            passive = attributes.PASSIVE_NO_FETCH_RELATED
        else:
            passive = attributes.PASSIVE_OFF

        for s in states:
            # TODO: add a high speed method
            # to InstanceState which returns:  attribute
            # has a non-None value, or had one
            history = uowcommit.get_attribute_history(s, self.key, passive)
            if history and not history.empty():
                return True
        else:
            return (
                states
                and not self.prop._is_self_referential
                and self.mapper in uowcommit.mappers
            )

    def _verify_canload(self, state):
        if self.prop.uselist and state is None:
            raise exc.FlushError(
                "Can't flush None value found in "
                "collection %s" % (self.prop,)
            )
        elif state is not None and not self.mapper._canload(
            state, allow_subtypes=not self.enable_typechecks
        ):
            if self.mapper._canload(state, allow_subtypes=True):
                raise exc.FlushError(
                    "Attempting to flush an item of type "
                    "%(x)s as a member of collection "
                    '"%(y)s". Expected an object of type '
                    "%(z)s or a polymorphic subclass of "
                    "this type. If %(x)s is a subclass of "
                    '%(z)s, configure mapper "%(zm)s" to '
                    "load this subtype polymorphically, or "
                    "set enable_typechecks=False to allow "
                    "any subtype to be accepted for flush. "
                    % {
                        "x": state.class_,
                        "y": self.prop,
                        "z": self.mapper.class_,
                        "zm": self.mapper,
                    }
                )
            else:
                raise exc.FlushError(
                    "Attempting to flush an item of type "
                    "%(x)s as a member of collection "
                    '"%(y)s". Expected an object of type '
                    "%(z)s or a polymorphic subclass of "
                    "this type."
                    % {
                        "x": state.class_,
                        "y": self.prop,
                        "z": self.mapper.class_,
                    }
                )

    def _synchronize(self, state, child, associationrow, clearkeys, uowcommit):
        raise NotImplementedError()

    def _get_reversed_processed_set(self, uow):
        if not self.prop._reverse_property:
            return None

        process_key = tuple(
            sorted([self.key] + [p.key for p in self.prop._reverse_property])
        )
        return uow.memo(("reverse_key", process_key), set)

    def _post_update(self, state, uowcommit, related, is_m2o_delete=False):
        for x in related:
            if not is_m2o_delete or x is not None:
                uowcommit.register_post_update(
                    state, [r for l, r in self.prop.synchronize_pairs]
                )
                break

    def _pks_changed(self, uowcommit, state):
        raise NotImplementedError()

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.prop)


class OneToManyDP(DependencyProcessor):
    def per_property_dependencies(
        self,
        uow,
        parent_saves,
        child_saves,
        parent_deletes,
        child_deletes,
        after_save,
        before_delete,
    ):
        if self.post_update:
            child_post_updates = unitofwork.PostUpdateAll(
                uow, self.mapper.primary_base_mapper, False
            )
            child_pre_updates = unitofwork.PostUpdateAll(
                uow, self.mapper.primary_base_mapper, True
            )

            uow.dependencies.update(
                [
                    (child_saves, after_save),
                    (parent_saves, after_save),
                    (after_save, child_post_updates),
                    (before_delete, child_pre_updates),
                    (child_pre_updates, parent_deletes),
                    (child_pre_updates, child_deletes),
                ]
            )
        else:
            uow.dependencies.update(
                [
                    (parent_saves, after_save),
                    (after_save, child_saves),
                    (after_save, child_deletes),
                    (child_saves, parent_deletes),
                    (child_deletes, parent_deletes),
                    (before_delete, child_saves),
                    (before_delete, child_deletes),
                ]
            )

    def per_state_dependencies(
        self,
        uow,
        save_parent,
        delete_parent,
        child_action,
        after_save,
        before_delete,
        isdelete,
        childisdelete,
    ):

        if self.post_update:

            child_post_updates = unitofwork.PostUpdateAll(
                uow, self.mapper.primary_base_mapper, False
            )
            child_pre_updates = unitofwork.PostUpdateAll(
                uow, self.mapper.primary_base_mapper, True
            )

            # TODO: this whole block is not covered
            # by any tests
            if not isdelete:
                if childisdelete:
                    uow.dependencies.update(
                        [
                            (child_action, after_save),
                            (after_save, child_post_updates),
                        ]
                    )
                else:
                    uow.dependencies.update(
                        [
                            (save_parent, after_save),
                            (child_action, after_save),
                            (after_save, child_post_updates),
                        ]
                    )
            else:
                if childisdelete:
                    uow.dependencies.update(
                        [
                            (before_delete, child_pre_updates),
                            (child_pre_updates, delete_parent),
                        ]
                    )
                else:
                    uow.dependencies.update(
                        [
                            (before_delete, child_pre_updates),
                            (child_pre_updates, delete_parent),
                        ]
                    )
        elif not isdelete:
            uow.dependencies.update(
                [
                    (save_parent, after_save),
                    (after_save, child_action),
                    (save_parent, child_action),
                ]
            )
        else:
            uow.dependencies.update(
                [(before_delete, child_action), (child_action, delete_parent)]
            )

    def presort_deletes(self, uowcommit, states):
        # head object is being deleted, and we manage its list of
        # child objects the child objects have to have their
        # foreign key to the parent set to NULL
        should_null_fks = (
            not self.cascade.delete and not self.passive_deletes == "all"
        )

        for state in states:
            history = uowcommit.get_attribute_history(
                state, self.key, self._passive_delete_flag
            )
            if history:
                for child in history.deleted:
                    if child is not None and self.hasparent(child) is False:
                        if self.cascade.delete_orphan:
                            uowcommit.register_object(child, isdelete=True)
                        else:
                            uowcommit.register_object(child)

                if should_null_fks:
                    for child in history.unchanged:
                        if child is not None:
                            uowcommit.register_object(
                                child, operation="delete", prop=self.prop
                            )

    def presort_saves(self, uowcommit, states):
        children_added = uowcommit.memo(("children_added", self), set)

        should_null_fks = (
            not self.cascade.delete_orphan
            and not self.passive_deletes == "all"
        )

        for state in states:
            pks_changed = self._pks_changed(uowcommit, state)

            if not pks_changed or self.passive_updates:
                passive = attributes.PASSIVE_NO_INITIALIZE
            else:
                passive = attributes.PASSIVE_OFF

            history = uowcommit.get_attribute_history(state, self.key, passive)
            if history:
                for child in history.added:
                    if child is not None:
                        uowcommit.register_object(
                            child,
                            cancel_delete=True,
                            operation="add",
                            prop=self.prop,
                        )

                children_added.update(history.added)

                for child in history.deleted:
                    if not self.cascade.delete_orphan:
                        if should_null_fks:
                            uowcommit.register_object(
                                child,
                                isdelete=False,
                                operation="delete",
                                prop=self.prop,
                            )
                    elif self.hasparent(child) is False:
                        uowcommit.register_object(
                            child,
                            isdelete=True,
                            operation="delete",
                            prop=self.prop,
                        )
                        for c, m, st_, dct_ in self.mapper.cascade_iterator(
                            "delete", child
                        ):
                            uowcommit.register_object(st_, isdelete=True)

            if pks_changed:
                if history:
                    for child in history.unchanged:
                        if child is not None:
                            uowcommit.register_object(
                                child,
                                False,
                                self.passive_updates,
                                operation="pk change",
                                prop=self.prop,
                            )

    def process_deletes(self, uowcommit, states):
        # head object is being deleted, and we manage its list of
        # child objects the child objects have to have their foreign
        # key to the parent set to NULL this phase can be called
        # safely for any cascade but is unnecessary if delete cascade
        # is on.

        if self.post_update or not self.passive_deletes == "all":
            children_added = uowcommit.memo(("children_added", self), set)

            for state in states:
                history = uowcommit.get_attribute_history(
                    state, self.key, self._passive_delete_flag
                )
                if history:
                    for child in history.deleted:
                        if (
                            child is not None
                            and self.hasparent(child) is False
                        ):
                            self._synchronize(
                                state, child, None, True, uowcommit, False
                            )
                            if self.post_update and child:
                                self._post_update(child, uowcommit, [state])

                    if self.post_update or not self.cascade.delete:
                        for child in set(history.unchanged).difference(
                            children_added
                        ):
                            if child is not None:
                                self._synchronize(
                                    state, child, None, True, uowcommit, False
                                )
                                if self.post_update and child:
                                    self._post_update(
                                        child, uowcommit, [state]
                                    )

                    # technically, we can even remove each child from the
                    # collection here too.  but this would be a somewhat
                    # inconsistent behavior since it wouldn't happen
                    # if the old parent wasn't deleted but child was moved.

    def process_saves(self, uowcommit, states):
        should_null_fks = (
            not self.cascade.delete_orphan
            and not self.passive_deletes == "all"
        )

        for state in states:
            history = uowcommit.get_attribute_history(
                state, self.key, attributes.PASSIVE_NO_INITIALIZE
            )
            if history:
                for child in history.added:
                    self._synchronize(
                        state, child, None, False, uowcommit, False
                    )
                    if child is not None and self.post_update:
                        self._post_update(child, uowcommit, [state])

                for child in history.deleted:
                    if (
                        should_null_fks
                        and not self.cascade.delete_orphan
                        and not self.hasparent(child)
                    ):
                        self._synchronize(
                            state, child, None, True, uowcommit, False
                        )

                if self._pks_changed(uowcommit, state):
                    for child in history.unchanged:
                        self._synchronize(
                            state, child, None, False, uowcommit, True
                        )

    def _synchronize(
        self, state, child, associationrow, clearkeys, uowcommit, pks_changed
    ):
        source = state
        dest = child
        self._verify_canload(child)
        if dest is None or (
            not self.post_update and uowcommit.is_deleted(dest)
        ):
            return
        if clearkeys:
            sync.clear(dest, self.mapper, self.prop.synchronize_pairs)
        else:
            sync.populate(
                source,
                self.parent,
                dest,
                self.mapper,
                self.prop.synchronize_pairs,
                uowcommit,
                self.passive_updates and pks_changed,
            )

    def _pks_changed(self, uowcommit, state):
        return sync.source_modified(
            uowcommit, state, self.parent, self.prop.synchronize_pairs
        )


class ManyToOneDP(DependencyProcessor):
    def __init__(self, prop):
        DependencyProcessor.__init__(self, prop)
        for mapper in self.mapper.self_and_descendants:
            mapper._dependency_processors.append(DetectKeySwitch(prop))

    def per_property_dependencies(
        self,
        uow,
        parent_saves,
        child_saves,
        parent_deletes,
        child_deletes,
        after_save,
        before_delete,
    ):

        if self.post_update:
            parent_post_updates = unitofwork.PostUpdateAll(
                uow, self.parent.primary_base_mapper, False
            )
            parent_pre_updates = unitofwork.PostUpdateAll(
                uow, self.parent.primary_base_mapper, True
            )

            uow.dependencies.update(
                [
                    (child_saves, after_save),
                    (parent_saves, after_save),
                    (after_save, parent_post_updates),
                    (after_save, parent_pre_updates),
                    (before_delete, parent_pre_updates),
                    (parent_pre_updates, child_deletes),
                    (parent_pre_updates, parent_deletes),
                ]
            )
        else:
            uow.dependencies.update(
                [
                    (child_saves, after_save),
                    (after_save, parent_saves),
                    (parent_saves, child_deletes),
                    (parent_deletes, child_deletes),
                ]
            )

    def per_state_dependencies(
        self,
        uow,
        save_parent,
        delete_parent,
        child_action,
        after_save,
        before_delete,
        isdelete,
        childisdelete,
    ):

        if self.post_update:

            if not isdelete:
                parent_post_updates = unitofwork.PostUpdateAll(
                    uow, self.parent.primary_base_mapper, False
                )
                if childisdelete:
                    uow.dependencies.update(
                        [
                            (after_save, parent_post_updates),
                            (parent_post_updates, child_action),
                        ]
                    )
                else:
                    uow.dependencies.update(
                        [
                            (save_parent, after_save),
                            (child_action, after_save),
                            (after_save, parent_post_updates),
                        ]
                    )
            else:
                parent_pre_updates = unitofwork.PostUpdateAll(
                    uow, self.parent.primary_base_mapper, True
                )

                uow.dependencies.update(
                    [
                        (before_delete, parent_pre_updates),
                        (parent_pre_updates, delete_parent),
                        (parent_pre_updates, child_action),
                    ]
                )

        elif not isdelete:
            if not childisdelete:
                uow.dependencies.update(
                    [(child_action, after_save), (after_save, save_parent)]
                )
            else:
                uow.dependencies.update([(after_save, save_parent)])

        else:
            if childisdelete:
                uow.dependencies.update([(delete_parent, child_action)])

    def presort_deletes(self, uowcommit, states):
        if self.cascade.delete or self.cascade.delete_orphan:
            for state in states:
                history = uowcommit.get_attribute_history(
                    state, self.key, self._passive_delete_flag
                )
                if history:
                    if self.cascade.delete_orphan:
                        todelete = history.sum()
                    else:
                        todelete = history.non_deleted()
                    for child in todelete:
                        if child is None:
                            continue
                        uowcommit.register_object(
                            child,
                            isdelete=True,
                            operation="delete",
                            prop=self.prop,
                        )
                        t = self.mapper.cascade_iterator("delete", child)
                        for c, m, st_, dct_ in t:
                            uowcommit.register_object(st_, isdelete=True)

    def presort_saves(self, uowcommit, states):
        for state in states:
            uowcommit.register_object(state, operation="add", prop=self.prop)
            if self.cascade.delete_orphan:
                history = uowcommit.get_attribute_history(
                    state, self.key, self._passive_delete_flag
                )
                if history:
                    for child in history.deleted:
                        if self.hasparent(child) is False:
                            uowcommit.register_object(
                                child,
                                isdelete=True,
                                operation="delete",
                                prop=self.prop,
                            )

                            t = self.mapper.cascade_iterator("delete", child)
                            for c, m, st_, dct_ in t:
                                uowcommit.register_object(st_, isdelete=True)

    def process_deletes(self, uowcommit, states):
        if (
            self.post_update
            and not self.cascade.delete_orphan
            and not self.passive_deletes == "all"
        ):

            # post_update means we have to update our
            # row to not reference the child object
            # before we can DELETE the row
            for state in states:
                self._synchronize(state, None, None, True, uowcommit)
                if state and self.post_update:
                    history = uowcommit.get_attribute_history(
                        state, self.key, self._passive_delete_flag
                    )
                    if history:
                        self._post_update(
                            state, uowcommit, history.sum(), is_m2o_delete=True
                        )

    def process_saves(self, uowcommit, states):
        for state in states:
            history = uowcommit.get_attribute_history(
                state, self.key, attributes.PASSIVE_NO_INITIALIZE
            )
            if history:
                if history.added:
                    for child in history.added:
                        self._synchronize(
                            state, child, None, False, uowcommit, "add"
                        )
                elif history.deleted:
                    self._synchronize(
                        state, None, None, True, uowcommit, "delete"
                    )
                if self.post_update:
                    self._post_update(state, uowcommit, history.sum())

    def _synchronize(
        self,
        state,
        child,
        associationrow,
        clearkeys,
        uowcommit,
        operation=None,
    ):
        if state is None or (
            not self.post_update and uowcommit.is_deleted(state)
        ):
            return

        if (
            operation is not None
            and child is not None
            and not uowcommit.session._contains_state(child)
        ):
            util.warn(
                "Object of type %s not in session, %s "
                "operation along '%s' won't proceed"
                % (mapperutil.state_class_str(child), operation, self.prop)
            )
            return

        if clearkeys or child is None:
            sync.clear(state, self.parent, self.prop.synchronize_pairs)
        else:
            self._verify_canload(child)
            sync.populate(
                child,
                self.mapper,
                state,
                self.parent,
                self.prop.synchronize_pairs,
                uowcommit,
                False,
            )


class DetectKeySwitch(DependencyProcessor):
    """For many-to-one relationships with no one-to-many backref,
    searches for parents through the unit of work when a primary
    key has changed and updates them.

    Theoretically, this approach could be expanded to support transparent
    deletion of objects referenced via many-to-one as well, although
    the current attribute system doesn't do enough bookkeeping for this
    to be efficient.

    """

    def per_property_preprocessors(self, uow):
        if self.prop._reverse_property:
            if self.passive_updates:
                return
            else:
                if False in (
                    prop.passive_updates
                    for prop in self.prop._reverse_property
                ):
                    return

        uow.register_preprocessor(self, False)

    def per_property_flush_actions(self, uow):
        parent_saves = unitofwork.SaveUpdateAll(uow, self.parent.base_mapper)
        after_save = unitofwork.ProcessAll(uow, self, False, False)
        uow.dependencies.update([(parent_saves, after_save)])

    def per_state_flush_actions(self, uow, states, isdelete):
        pass

    def presort_deletes(self, uowcommit, states):
        pass

    def presort_saves(self, uow, states):
        if not self.passive_updates:
            # for non-passive updates, register in the preprocess stage
            # so that mapper save_obj() gets a hold of changes
            self._process_key_switches(states, uow)

    def prop_has_changes(self, uow, states, isdelete):
        if not isdelete and self.passive_updates:
            d = self._key_switchers(uow, states)
            return bool(d)

        return False

    def process_deletes(self, uowcommit, states):
        assert False

    def process_saves(self, uowcommit, states):
        # for passive updates, register objects in the process stage
        # so that we avoid ManyToOneDP's registering the object without
        # the listonly flag in its own preprocess stage (results in UPDATE)
        # statements being emitted
        assert self.passive_updates
        self._process_key_switches(states, uowcommit)

    def _key_switchers(self, uow, states):
        switched, notswitched = uow.memo(
            ("pk_switchers", self), lambda: (set(), set())
        )

        allstates = switched.union(notswitched)
        for s in states:
            if s not in allstates:
                if self._pks_changed(uow, s):
                    switched.add(s)
                else:
                    notswitched.add(s)
        return switched

    def _process_key_switches(self, deplist, uowcommit):
        switchers = self._key_switchers(uowcommit, deplist)
        if switchers:
            # if primary key values have actually changed somewhere, perform
            # a linear search through the UOW in search of a parent.
            for state in uowcommit.session.identity_map.all_states():
                if not issubclass(state.class_, self.parent.class_):
                    continue
                dict_ = state.dict
                related = state.get_impl(self.key).get(
                    state, dict_, passive=self._passive_update_flag
                )
                if (
                    related is not attributes.PASSIVE_NO_RESULT
                    and related is not None
                ):
                    if self.prop.uselist:
                        if not related:
                            continue
                        related_obj = related[0]
                    else:
                        related_obj = related
                    related_state = attributes.instance_state(related_obj)
                    if related_state in switchers:
                        uowcommit.register_object(
                            state, False, self.passive_updates
                        )
                        sync.populate(
                            related_state,
                            self.mapper,
                            state,
                            self.parent,
                            self.prop.synchronize_pairs,
                            uowcommit,
                            self.passive_updates,
                        )

    def _pks_changed(self, uowcommit, state):
        return bool(state.key) and sync.source_modified(
            uowcommit, state, self.mapper, self.prop.synchronize_pairs
        )


class ManyToManyDP(DependencyProcessor):
    def per_property_dependencies(
        self,
        uow,
        parent_saves,
        child_saves,
        parent_deletes,
        child_deletes,
        after_save,
        before_delete,
    ):

        uow.dependencies.update(
            [
                (parent_saves, after_save),
                (child_saves, after_save),
                (after_save, child_deletes),
                # a rowswitch on the parent from  deleted to saved
                # can make this one occur, as the "save" may remove
                # an element from the
                # "deleted" list before we have a chance to
                # process its child rows
                (before_delete, parent_saves),
                (before_delete, parent_deletes),
                (before_delete, child_deletes),
                (before_delete, child_saves),
            ]
        )

    def per_state_dependencies(
        self,
        uow,
        save_parent,
        delete_parent,
        child_action,
        after_save,
        before_delete,
        isdelete,
        childisdelete,
    ):
        if not isdelete:
            if childisdelete:
                uow.dependencies.update(
                    [(save_parent, after_save), (after_save, child_action)]
                )
            else:
                uow.dependencies.update(
                    [(save_parent, after_save), (child_action, after_save)]
                )
        else:
            uow.dependencies.update(
                [(before_delete, child_action), (before_delete, delete_parent)]
            )

    def presort_deletes(self, uowcommit, states):
        # TODO: no tests fail if this whole
        # thing is removed !!!!
        if not self.passive_deletes:
            # if no passive deletes, load history on
            # the collection, so that prop_has_changes()
            # returns True
            for state in states:
                uowcommit.get_attribute_history(
                    state, self.key, self._passive_delete_flag
                )

    def presort_saves(self, uowcommit, states):
        if not self.passive_updates:
            # if no passive updates, load history on
            # each collection where parent has changed PK,
            # so that prop_has_changes() returns True
            for state in states:
                if self._pks_changed(uowcommit, state):
                    history = uowcommit.get_attribute_history(
                        state, self.key, attributes.PASSIVE_OFF
                    )

        if not self.cascade.delete_orphan:
            return

        # check for child items removed from the collection
        # if delete_orphan check is turned on.
        for state in states:
            history = uowcommit.get_attribute_history(
                state, self.key, attributes.PASSIVE_NO_INITIALIZE
            )
            if history:
                for child in history.deleted:
                    if self.hasparent(child) is False:
                        uowcommit.register_object(
                            child,
                            isdelete=True,
                            operation="delete",
                            prop=self.prop,
                        )
                        for c, m, st_, dct_ in self.mapper.cascade_iterator(
                            "delete", child
                        ):
                            uowcommit.register_object(st_, isdelete=True)

    def process_deletes(self, uowcommit, states):
        secondary_delete = []
        secondary_insert = []
        secondary_update = []

        processed = self._get_reversed_processed_set(uowcommit)
        tmp = set()
        for state in states:
            # this history should be cached already, as
            # we loaded it in preprocess_deletes
            history = uowcommit.get_attribute_history(
                state, self.key, self._passive_delete_flag
            )
            if history:
                for child in history.non_added():
                    if child is None or (
                        processed is not None and (state, child) in processed
                    ):
                        continue
                    associationrow = {}
                    if not self._synchronize(
                        state,
                        child,
                        associationrow,
                        False,
                        uowcommit,
                        "delete",
                    ):
                        continue
                    secondary_delete.append(associationrow)

                tmp.update((c, state) for c in history.non_added())

        if processed is not None:
            processed.update(tmp)

        self._run_crud(
            uowcommit, secondary_insert, secondary_update, secondary_delete
        )

    def process_saves(self, uowcommit, states):
        secondary_delete = []
        secondary_insert = []
        secondary_update = []

        processed = self._get_reversed_processed_set(uowcommit)
        tmp = set()

        for state in states:
            need_cascade_pks = not self.passive_updates and self._pks_changed(
                uowcommit, state
            )
            if need_cascade_pks:
                passive = attributes.PASSIVE_OFF
            else:
                passive = attributes.PASSIVE_NO_INITIALIZE
            history = uowcommit.get_attribute_history(state, self.key, passive)
            if history:
                for child in history.added:
                    if processed is not None and (state, child) in processed:
                        continue
                    associationrow = {}
                    if not self._synchronize(
                        state, child, associationrow, False, uowcommit, "add"
                    ):
                        continue
                    secondary_insert.append(associationrow)
                for child in history.deleted:
                    if processed is not None and (state, child) in processed:
                        continue
                    associationrow = {}
                    if not self._synchronize(
                        state,
                        child,
                        associationrow,
                        False,
                        uowcommit,
                        "delete",
                    ):
                        continue
                    secondary_delete.append(associationrow)

                tmp.update((c, state) for c in history.added + history.deleted)

                if need_cascade_pks:

                    for child in history.unchanged:
                        associationrow = {}
                        sync.update(
                            state,
                            self.parent,
                            associationrow,
                            "old_",
                            self.prop.synchronize_pairs,
                        )
                        sync.update(
                            child,
                            self.mapper,
                            associationrow,
                            "old_",
                            self.prop.secondary_synchronize_pairs,
                        )

                        secondary_update.append(associationrow)

        if processed is not None:
            processed.update(tmp)

        self._run_crud(
            uowcommit, secondary_insert, secondary_update, secondary_delete
        )

    def _run_crud(
        self, uowcommit, secondary_insert, secondary_update, secondary_delete
    ):
        connection = uowcommit.transaction.connection(self.mapper)

        if secondary_delete:
            associationrow = secondary_delete[0]
            statement = self.secondary.delete().where(
                sql.and_(
                    *[
                        c == sql.bindparam(c.key, type_=c.type)
                        for c in self.secondary.c
                        if c.key in associationrow
                    ]
                )
            )
            result = connection.execute(statement, secondary_delete)

            if (
                result.supports_sane_multi_rowcount()
            ) and result.rowcount != len(secondary_delete):
                raise exc.StaleDataError(
                    "DELETE statement on table '%s' expected to delete "
                    "%d row(s); Only %d were matched."
                    % (
                        self.secondary.description,
                        len(secondary_delete),
                        result.rowcount,
                    )
                )

        if secondary_update:
            associationrow = secondary_update[0]
            statement = self.secondary.update(
                sql.and_(
                    *[
                        c == sql.bindparam("old_" + c.key, type_=c.type)
                        for c in self.secondary.c
                        if c.key in associationrow
                    ]
                )
            )
            result = connection.execute(statement, secondary_update)

            if (
                result.supports_sane_multi_rowcount()
            ) and result.rowcount != len(secondary_update):
                raise exc.StaleDataError(
                    "UPDATE statement on table '%s' expected to update "
                    "%d row(s); Only %d were matched."
                    % (
                        self.secondary.description,
                        len(secondary_update),
                        result.rowcount,
                    )
                )

        if secondary_insert:
            statement = self.secondary.insert()
            connection.execute(statement, secondary_insert)

    def _synchronize(
        self, state, child, associationrow, clearkeys, uowcommit, operation
    ):

        # this checks for None if uselist=True
        self._verify_canload(child)

        # but if uselist=False we get here.   If child is None,
        # no association row can be generated, so return.
        if child is None:
            return False

        if child is not None and not uowcommit.session._contains_state(child):
            if not child.deleted:
                util.warn(
                    "Object of type %s not in session, %s "
                    "operation along '%s' won't proceed"
                    % (mapperutil.state_class_str(child), operation, self.prop)
                )
            return False

        sync.populate_dict(
            state, self.parent, associationrow, self.prop.synchronize_pairs
        )
        sync.populate_dict(
            child,
            self.mapper,
            associationrow,
            self.prop.secondary_synchronize_pairs,
        )

        return True

    def _pks_changed(self, uowcommit, state):
        return sync.source_modified(
            uowcommit, state, self.parent, self.prop.synchronize_pairs
        )


_direction_to_processor = {
    ONETOMANY: OneToManyDP,
    MANYTOONE: ManyToOneDP,
    MANYTOMANY: ManyToManyDP,
}
