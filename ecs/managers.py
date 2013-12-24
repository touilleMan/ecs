"""Entity and System Managers."""

from ecs.exceptions import (
    NonexistentComponentTypeForEntity, DuplicateSystemTypeError)
from ecs.models import Entity


class EntityManager(object):
    """Provide database-like access to components based on an entity key."""
    def __init__(self):
        self._database = {}
        self._next_guid = 0

    @property
    def database(self):
        """Get this manager's database. Direct modification is not
        permitted.

        :return: the database
        :rtype: :class:`dict`
        """
        return self._database

    def create_entity(self):
        """Return a new entity instance with the current lowest GUID value.
        Does not store a reference to it, and does not make any entries in the
        database referencing it.

        :return: the new entity
        :rtype: :class:`ecs.models.Entity`
        """
        entity = Entity(self._next_guid)
        self._next_guid += 1
        return entity

    def add_component(self, entity_id, component_instance):
        """Add a component to the database and associates it with the given
        ``entity_id``. ``entity_id`` can be an :class:`ecs.models.Entity`
        object or a plain :class:`int`.

        :param entity_id: GUID of the entity
        :type entity_id: :class:`int` or :class:`ecs.models.Entity`
        :param component_instance: component to add to the entity
        :type component_instance: :class:`ecs.models.Component`
        """
        component_type = type(component_instance)
        if component_type not in self._database:
            self._database[component_type] = {}

        self._database[component_type][entity_id] = component_instance

    def remove_component(self, entity_id, component_type):
        """Remove the component of ``component_type`` associated with
        ``entity_id`` from the database. Doesn't do any kind of data-teardown.
        It is up to the system calling this code to do that. In the future,
        a callback system may be used to implement type-specific destructors.

        :param entity_id: GUID of the entity
        :type entity_id: :class:`int`
        :param component_type: component to remove from the entity
        :type component_type: :class:`ecs.models.Component`
        """
        try:
            del self._database[component_type][entity_id]
            if self._database[component_type] == {}:
                del self._database[component_type]
        except KeyError:
            pass

    def pairs_for_type(self, component_type):
        """Return a list of ``(entity_id, component_instance)`` tuples for all
        entities in the database possessing a component of ``component_type``.
        Return an empty list if there are no components of this type in the
        database. Can use in a loop like this, where ``Renderable`` is a
        component type:

        .. code-block:: python

            for entity, renderable_component in \
entity_manager.pairs_for_type(Renderable):
                pass # do something

        :param component_type: a type of created component
        :type component_type: :class:`type`
        :return: list of ``(entity_id, component_instance)`` tuples
        :rtype: :class:`tuple` of (:class:`int`, :class:`ecs.models.Component`)
        """
        try:
            return self._database[component_type].items()
        except KeyError:
            return []

    def component_for_entity(self, entity_id, component_type):
        """Return the instance of ``component_type`` for the ``entity_id``
        from the database.

        :param entity_id: entity GUID
        :type entity_id: :class:`int`
        :param component_type: a type of created component
        :type component_type: :class:`type`
        :return: list of ``(entity_id, component_instance)`` tuples
        :rtype: :class:`tuple` of (:class:`int`, :class:`ecs.models.Component`)
        :raises: :exc:`NonexistentComponentTypeForEntity` when \
        ``component_type`` does not exist on ``entity_instance``
        """
        try:
            return self._database[component_type][entity_id]
        except KeyError:
            raise NonexistentComponentTypeForEntity(
                entity_id, component_type)

    def remove_entity(self, entity_id):
        """Remove all components from the database that are associated with
        ``entity_id``, with the side-effect that the entity is also no longer
        in the database.

        :param entity_id: entity GUID
        :type entity_id: :class:`int`
        """
        # Don't use iterkeys(), otherwise we will get a RuntimeError about
        # mutating the length of the dictionary at runtime.
        for comp_type in self._database.keys():
            try:
                del self._database[comp_type][entity_id]
                if self._database[comp_type] == {}:
                    del self._database[comp_type]
            except KeyError:
                pass


class SystemManager(object):
    """A container and manager for :class:`ecs.models.System` objects."""
    def __init__(self):
        self._systems = []
        self._system_types = {}

    # Allow getting the list of systems but not directly setting it.
    @property
    def systems(self):
        """Get this manager's list of systems.

        :return: system list
        :rtype: :class:`list` of :class:`ecs.models.System`
        """
        return self._systems

    def add_system(self, system_instance):
        """Add a :class:`ecs.models.System` instance to the manager.

        :param system_instance: instance of a system
        :type system_instance: :class:`ecs.models.System`
        """
        system_type = type(system_instance)
        if system_type in self._system_types:
            raise DuplicateSystemTypeError(system_type)
        self._system_types[system_type] = system_instance
        self._systems.append(system_instance)

    def remove_system(self, system_type):
        """Tell the manager to no longer run the system of this type.

        :param system_type: type of system to remove
        :type system_type: :class:`type`
        """
        self._systems.remove(self._system_types[system_type])
        del self._system_types[system_type]

    def update(self, dt):
        """Run all systems in order, for this frame.

        :param dt: delta time, or elapsed time for this frame
        :type dt: :class:`float`
        """
        # Iterating over a list of systems instead of values in a dictionary is
        # noticeably faster. We maintain a list in addition to a dictionary
        # specifically for this purpose.
        for system in self._systems:
            system.update(dt)
