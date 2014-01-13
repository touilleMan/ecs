"""Exceptions that may be raised."""


class NonexistentComponentTypeForEntity(Exception):
    """Error indicating that a component type does not exist for a certain
    entity."""
    def __init__(self, entity, component_type):
        """:param entity: entity without component type
        :type entity: :class:`Entity`
        :param component_type: component type not in entity
        :type component_type: :class:`type`
        """
        self.entity = entity
        self.component_type = component_type

    def __str__(self):
        return "Nonexistent component type: `{0}' for entity: `{1}'".format(
            self.component_type.__name__, self.entity)


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


class SystemAlreadyAddedToManagerError(Exception):
    """Error indicating that a system is already part of a system manager."""
    def __init__(self, system, existing_system_manager, new_system_manager):
        """:param system: system attempted to be added
        :type system: :class:`ecs.models.System`
        :param existing_system_manager: manager which already owns system
        :type existing_system_manager: :class:`ecs.managers.SystemManager`
        :param new_system_manager: manager to which system was attempted to be
            added
        :type new_system_manager: :class:`ecs.managers.SystemManager`
        """
        self.system = system
        self.existing_system_manager = existing_system_manager
        self.new_system_manager = new_system_manager

    def __str__(self):
        return (
            "System `{0}' which belongs to system manager `{1}'"
            "attempted to be added to system manager `{2}'").format(
            self.system, self.existing_system_manager,
            self.new_system_manager)
