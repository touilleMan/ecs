""":mod:`ecs.entity` -- Entity definitions
"""


class Entity(object):
    """Encapsulates a GUID to use in the entity database.
    """
    def __init__(self, guid):
        """:param guid: globally unique identifier
        :type guid: :class:`int`
        """
        self.__guid_ = guid

    def __str__(self):
        """Stringify.

        :return: GUID as a string
        :rtype: :class:`str`
        """
        return str(self.__guid_)

    def __hash__(self):
        """Hash function for this object.

        :return: the hash value
        :rtype: :class:`int`
        """
        return self.__guid_

    def __eq__(self, other):
        """Equality method.

        :param other: other entity
        :type other: :class:`Entity`
        :return: ``True`` if equal
        :rtype: :class:`bool`
        """
        return self.__guid_ == hash(other)


class EntityManager(object):
    """Provides database-like access to components based on an ``entity_id``
    key.
    """
    def __init__(self):
        self.database = {}
        self.lowest_guid = 0

    def new_entity(self):
        """Returns a new entity instance with the current lowest GUID value.
        Does not store a reference to it, and does not make any entries in the
        database referencing it.

        :return: the new entity
        :rtype: :class:`Entity`
        """
        new_e = Entity(self.lowest_guid)
        self.lowest_guid += 1
        return new_e

    def add_component(self, entity_id, component_instance):
        """Adds a component to the database and associates it with the given
        ``entity_id``. ``entity_id`` can be an :class:`Entity` object or a
        plain :class:`int`.

        :param entity_id: GUID of the entity
        :type entity_id: :class:`int`
        :param component_instance: component to add to the entity
        :type component_instance: :class:`Component`

        """
        main_key = type(component_instance)
        if main_key not in self.database:
                self.database[main_key] = {}

        self.database[main_key][entity_id] = component_instance

    def remove_component(self, entity_id, component_type):
        """Removes the component of component_type associated with entity_id
        from the database. Doesn't do any kind of data-teardown. It is up to
        the system calling this code to do that. In the future a callback
        system may be used to implement type-specific destructors.

        :param entity_id: GUID of the entity
        :type entity_id: :class:`int`
        :param component_instance: component to remove from the entity
        :type component_instance: :class:`Component`
        """
        try:
            del self.database[component_type][entity_id]
            if self.database[component_type] == {}:
                del self.database[component_type]
        except KeyError:
            pass

    def pairs_for_type(self, component_type):
        """Returns a list of ``(entity_id, component_instance)`` tuples for all
        entities in the database possessing a component of ``component_type``.
        Returns ``None`` if there are no components of this type in the
        database. Can use in a loop like this, where ``Renderable`` is a
        component type:

        .. code-block:: python

            for entity, renderable_component in \
entity_manager.pairs_for_type(Renderable):
                pass # do something

        :param component_type: a type of created component
        :type component_type: :class:`type`
        :return: list of ``(entity_id, component_instance)`` tuples
        :rtype: :class:`tuple` of (:class:`int`, :class:`Component`)
        """
        try:
            return self.database[component_type].items()
        except KeyError:
            return None

    def component_for_entity(self, entity_id, component_type):
        """Returns the instance of ``component_type`` for the ``entity_id``
        from the database. Returns ``None`` if the entity does not have that
        component.

        :param entity_id: entity GUID
        :type entity_id: :class:`int`
        :param component_type: a type of created component
        :type component_type: :class:`type`
        :return: list of ``(entity_id, component_instance)`` tuples
        :rtype: :class:`tuple` of (:class:`int`, :class:`Component`)
        """
        try:
            return self.database[component_type][entity_id]
        except KeyError:
            return None

    def delete_entity(self, entity_id):
        """Removes all components from the database that are associated with
        ``entity_id``, with the side-effect that the entity is also no longer
        in the database.

        :param entity_id: entity GUID
        :type entity_id: :class:`int`
        """
        for comp_type in self.database.iterkeys():
            try:
                del self.database[comp_type][entity_id]
                if self.database[comp_type] == {}:
                    del self.database[comp_type]
            except KeyError:
                pass
