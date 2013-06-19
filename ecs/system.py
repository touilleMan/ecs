""":mod:`ecs.system` --- System-related classes
"""


class DuplicateSystemTypeException(Exception):
    """Error raised when a system of an existing type is attempted to be added
    to the database.
    """
    pass


class System(object):
    """An object that represents an operation on a set of objects from the game
    database.
    """
    def __init__(self):
        # A reference to the SystemManager that holds this
        self.sys_man = None
        # just a placeholder for the system-manager to do what it will
        self.priority = 0

    def update(self, dt, entity_manager):
        """Called by the system manager. Here is where the functionality of
        the system is implemented.

        :param dt: delta time, or elapsed time for this frame
        :type dt: :class:`float`
        :param entity_manager: the entity manager to use
        :type entity_manager: :class:`EntityManager`
        """
        print 'System.update called. dt={}, entity_manager={}'.format(
            dt, entity_manager)


class SystemManager(object):
    """A container and manager for :class:`System` objects. Maintains a list of
    :class:`System` objects. Has a facility for updating those :class:`System`
    objects, in the order of priority.
    """
    def __init__(self, parent):
        """:param parent: a reference to the object that contains this manager
        :type parent: :class:`object`
        """
        self.parent = parent
        self._systems = []

    def add_system(self, system_instance, priority=0):
        """Adds a :class:`System` instance to the manager.  It will be updated
        according to the priority given, lower numbers first.

        :param system_instance: instance of a system
        :type system_instance: :class:`System`
        :param priority: affect the order in which to run the system
        :type priority: :class:`int`
        """
        if [True for s in self._systems if type(s) is type(system_instance)]:
            raise DuplicateSystemTypeException()

        system_instance.priority = priority
        system_instance.sys_man = self

        self._systems.append(system_instance)
        self._systems.sort(key=lambda s: s.priority)

    def remove_system(self, system_type):
        """Removes a :class:`System` instance of type ``system_type`` from the
        manager.

        :param system_type: type of system to remove
        :type system_type: :class:`type`
        """
        for s in self._systems:
            if type(s) is system_type:
                s.sys_man = None
                self._systems.remove(s)
                return

    def update_systems(self, dt, entity_manager):
        """Run each system, in the order of their priority.

        :param dt: delta time, or elapsed time for this frame
        :type dt: :class:`float`
        :param entity_manager: the entity manager to use
        :type entity_manager: :class:`EntityManager`
        """
        for system in self._systems:
            system.update(dt, entity_manager)
