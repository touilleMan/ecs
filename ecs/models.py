"""Entity, Component, and System classes."""

from __future__ import print_function
from abc import ABCMeta, abstractmethod


class Entity(object):
    """Encapsulation of a GUID to use in the entity database."""
    def __init__(self, guid):
        """:param guid: globally unique identifier
        :type guid: :class:`int`
        """
        self._guid = guid

    def __str__(self):
        """Stringify.

        :return: GUID as a string
        :rtype: :class:`str`
        """
        return str(self._guid)

    def __hash__(self):
        """Hash function for this object.

        :return: the hash value
        :rtype: :class:`int`
        """
        return self._guid

    def __eq__(self, other):
        """Equality method.

        :param other: other entity
        :type other: :class:`Entity`
        :return: ``True`` if equal
        :rtype: :class:`bool`
        """
        return self._guid == hash(other)


class Component(object):
    """Class from which all components should derive."""
    pass


class System(object):
    """An object that represents an operation on a set of objects from the game
    database. The :meth:`update` method must be implemented.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, dt):
        """Run the system for this frame. This method is called by the system
        manager, and is where the functionality of the system is implemented.

        :param dt: delta time, or elapsed time for this frame
        :type dt: :class:`float`
        """
        print("System's update() method was called "
              "with time delta of {}".format(dt))
