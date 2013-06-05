""":mod:`ecs` -- An entity system in Python
"""

from ecs import metadata
__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright

# Provide a common namespace for the entity, component, and system modules.
from ecs.entity import Entity, EntityManager  # NOQA
from ecs.system import (  # NOQA
    DuplicateSystemTypeException, System, SystemManager)
from ecs.component import Component  # NOQA
