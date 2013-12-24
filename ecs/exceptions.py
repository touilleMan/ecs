"""Exceptions that may be raised."""


class NonexistentComponentTypeForEntity(Exception):
    """Error indicating that a component type does not exist for a certain
    entity."""
    def __init__(self, entity_instance, component_type):
        """:param entity: entity without component type
        :type entity: :class:`Entity`
        :param component_type: component type not in entity
        :type component_type: :class:`type`
        """
        self.entity_instance = entity_instance
        self.component_type = component_type

    def __str__(self):
        return "Nonexistent component type: `{0}' for entity: `{1}'".format(
            self.component_type.__name__, self.entity_instance)


class DuplicateSystemTypeError(Exception):
    """Error indicating that the system type already exists in the system
    manager."""
    def __init__(self, system_type):
        """:param system_type: type of the system
        :type system_type: :class:`type`
        """
        self.system_type = system_type

    def __str__(self):
        return "Duplicate system type: `{0}'".format(self.system_type.__name__)
