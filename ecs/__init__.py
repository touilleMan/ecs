"""An entity/component system library for games."""

from ecs import metadata as _metadata
# Provide a common namespace for these classes.
from ecs.models import Entity, Component, System
from ecs.managers import EntityManager, SystemManager


__version__ = _metadata.version
__author__ = _metadata.authors[0]
__license__ = _metadata.license
__copyright__ = _metadata.copyright


__all__ = ['Entity', 'Component', 'System', 'EntityManager', 'SystemManager']
