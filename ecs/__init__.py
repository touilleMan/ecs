"""An entity/component system library for games."""

from ecs import metadata as _metadata
# Provide a common namespace for these classes.
from ecs.models import Entity, Component, System  # NOQA
from ecs.managers import EntityManager, SystemManager  # NOQA


__version__ = _metadata.version
__author__ = _metadata.authors[0]
__license__ = _metadata.license
__copyright__ = _metadata.copyright
