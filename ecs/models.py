"""Entity, Component, and System classes."""

from __future__ import print_function
from abc import ABCMeta, abstractmethod

import six


class Entity(object):
    """Encapsulation of a GUID to use in the entity database."""
    def __init__(self, guid):
        """:param guid: globally unique identifier
        :type guid: :class:`int`
        """
        self._guid = guid

    def __repr__(self):
        return '{0}({1})'.format(type(self).__name__, self._guid)

    def __hash__(self):
        return self._guid

    def __eq__(self, other):
        return self._guid == hash(other)


class Component(object):
    """Class from which all components should derive."""
    pass


@six.add_metaclass(ABCMeta)
class System(object):
    """An object that represents an operation on a set of objects from the game
    database. The :meth:`update` method must be implemented.
    """
    @abstractmethod
    def update(self, entity_manager, dt):
        """Run the system for this frame. This method is called by the system
        manager, and is where the functionality of the system is implemented.

        :param entity_manager: this system's entity manager, used for
            querying components
        :type entity_manager: :class:`ecs.managers.EntityManager`
        :param dt: delta time, or elapsed time for this frame
        :type dt: :class:`float`
        """
        six.print_("System's update() method was called: "
                   'entity_manager={0}, dt={1}'.format(entity_manager, dt))
