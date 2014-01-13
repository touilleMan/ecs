import re

from pytest import fixture, raises
import pytest
usefixtures = pytest.mark.usefixtures
from mock import MagicMock, sentinel

from ecs.models import Component, System
from ecs.managers import EntityManager, SystemManager
from ecs.exceptions import (
    NonexistentComponentTypeForEntity, DuplicateSystemTypeError,
    SystemAlreadyAddedToManagerError)

from tests.helpers import assert_exc_info_msg


class TestEntityManager(object):
    @fixture
    def manager(self):
        return EntityManager()

    @fixture
    def entities(self, manager):
        return [manager.create_entity() for _ in range(5)]

    @fixture
    def component_types(self):
        return [
            type('Component' + str(i), (Component,), {}) for i in range(5)]

    @fixture
    def components(self, component_types):
        # The last item is another component of type 0.
        return [type_() for type_ in component_types] + [component_types[0]()]

    @fixture(autouse=True)
    def setup_pairs(self, manager, entities, components):
        manager.add_component(entities[0], components[0])
        manager.add_component(entities[3], components[0])
        manager.add_component(entities[3], components[4])
        manager.add_component(entities[4], components[3])
        manager.add_component(entities[1], components[5])

    def test_create_new_entities(self, manager):
        # We should not test the implementation of the "hash", but just ensure
        # that entities of different IDs are being generated.
        num = 100
        entities = set([manager.create_entity() for _ in range(num)])
        assert len(entities) == num

    class TestPairsForType(object):
        def test_existing_component_type(
                self, manager, entities, components, component_types):
            assert list(manager.pairs_for_type(component_types[0])) == [
                (entities[0], components[0]),
                (entities[1], components[5]),
                (entities[3], components[0])]

        def test_nonexistent_component_type(
                self, manager, entities, component_types):
            assert list(manager.pairs_for_type(component_types[2])) == []

    class TestRemoveComponent(object):
        def test_remove_some_of_a_component(
                self, manager, entities, components, component_types):
            manager.remove_component(entities[3], component_types[0])
            assert manager.database == {
                component_types[0]: {
                    entities[0]: components[0],
                    entities[1]: components[5],
                },
                component_types[3]: {
                    entities[4]: components[3],
                },
                component_types[4]: {
                    entities[3]: components[4],
                }
            }

        def test_remove_all_of_a_component(
                self, manager, entities, components, component_types):
            manager.remove_component(entities[3], component_types[4])
            assert manager.database == {
                component_types[0]: {
                    entities[0]: components[0],
                    entities[3]: components[0],
                    entities[1]: components[5],
                },
                component_types[3]: {
                    entities[4]: components[3],
                },
            }

        def test_remove_nonexistent_relationship(
                self, manager, entities, components, component_types):
            db_before = manager.database
            manager.remove_component(entities[0], component_types[4])
            assert db_before == manager.database

    class TestComponentForEntityType(object):
        def test_normal_usage(
                self, manager, entities, components, component_types):
            assert manager.component_for_entity(
                entities[3], component_types[4]) == components[4]

        def test_raises_error_on_nonexistent_component_type(
                self, manager, entities, components, component_types):
            with raises(NonexistentComponentTypeForEntity) as exc_info:
                manager.component_for_entity(entities[3], component_types[1])
            assert_exc_info_msg(
                exc_info,
                "Nonexistent component type: "
                "`Component1' for entity: `Entity(3)'")

    def test_remove_entity(
            self, manager, entities, components, component_types):
        manager.remove_entity(entities[3])
        assert manager.database == {
            component_types[0]: {
                entities[0]: components[0], entities[1]: components[5]},
            component_types[3]: {entities[4]: components[3]},
        }


class TestSystemManager(object):
    @fixture
    def system_types(self):
        return [
            type('System' + str(i),
                 (System,),
                 {'update': MagicMock()})
            for i in range(5)]

    @fixture
    def systems(self, system_types):
        return [type_() for type_ in system_types]

    @fixture
    def manager(self, systems):
        sm = SystemManager(sentinel.entity_manager)
        for system in systems:
            sm.add_system(system)
        return sm

    class TestAddSystem(object):
        def test_systems_added(self, manager, systems):
            # add_system was called normally in the fixture.
            assert manager.systems == systems

        def test_entity_manager_set(self, manager):
            for system in manager.systems:
                assert system.entity_manager == sentinel.entity_manager

        def test_system_manager_set(self, manager):
            for system in manager.systems:
                assert system.system_manager == manager

        class TestDuplicate(object):
            def test_raises_error(self, manager, systems):
                with raises(DuplicateSystemTypeError) as exc_info:
                    manager.add_system(systems[1])
                assert_exc_info_msg(
                    exc_info, "Duplicate system type: `System1'")

            def test_system_and_entity_managers_not_set(
                    self, manager, system_types):
                system = system_types[0]()
                with raises(DuplicateSystemTypeError):
                    manager.add_system(system)
                assert system.entity_manager is None
                assert system.system_manager is None

        class TestSystemAlreadyAdded(object):
            def test_raises_error(self, manager, systems):
                manager2 = SystemManager(sentinel.entity_manager)
                with raises(SystemAlreadyAddedToManagerError) as exc_info:
                    manager2.add_system(systems[0])
                # It's going to format a memory address for each class. We
                # don't care about that.
                assert re.match(
                    "System `.*' which belongs to system manager `.*'"
                    "attempted to be added to system manager `.*'$",
                    str(exc_info.value))

            def test_system_and_entity_managers_not_changed(
                    self, manager, systems):
                manager2 = SystemManager(sentinel.entity_manager)
                with raises(SystemAlreadyAddedToManagerError):
                    manager2.add_system(systems[0])

                assert systems[0].entity_manager == sentinel.entity_manager
                assert systems[0].system_manager == manager

    class TestRemoveSystem(object):
        def test_remove_system(self, manager, systems, system_types):
            manager.remove_system(system_types[0])
            assert manager.systems == systems[1:]

        def test_entity_manager_unset(self, manager, systems, system_types):
            manager.remove_system(system_types[0])
            assert systems[0].entity_manager is None

        def test_system_manager_unset(self, manager, systems, system_types):
            manager.remove_system(system_types[0])
            assert systems[0].system_manager is None

    def test_update(self, manager, systems):
        manager.update(20)
        for system in systems:
            system.update.assert_called_once_with(20)
