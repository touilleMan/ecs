.. -*- coding: utf-8; -*-
.. UTF-8 is used for the em dash, en dash, and the hair space. Check out <http://csswizardry.com/2010/01/the-three-types-of-dash/>

ecs
===

.. image:: https://travis-ci.org/seanfisk/ecs.png
   :target: https://travis-ci.org/seanfisk/ecs

**ecs is an MIT-licensed Python entity/component system library for games.**

There are many articles on the Internet advocating a switch to entity-based systems for game logic. However, many authors seem to burn themselves out telling why the old inheritance-based approach is problematic and how an entity system will solve your problems — without ever really explaining what it is or how to do it. *This project attempts to provide an actual implementation for use in real games.*

The library is called an "entity/component system" library rather than an "entity system," as the entity portion is just one building block of the total concept.

The module is called ``ecs``. ``ces`` is too close to something else, and while there is another library called ``ecs``, it's for an E-Commerce service from Amazon and is unlikely to name-clash in your projects.

As this module is in somewhat rarefied air, with not a lot of company, the concepts and API may change during development. Inspiration is taken from the `Ash framework`_ for ActionScript 3.0 and `Artemis framework`_ for Java.

.. _Ash framework: http://www.ashframework.org/
.. _Artemis framework: http://gamadu.com/artemis/index.html

Concepts
--------

**ecs** stands for **Entity**, **Component**, and **System**. Each of these parts is important. So what are these?

**Entity**
    Simply a unique identifier, used to label components as belonging to a logical grouping.

**Component**
    A collection of data. Has no behavior associated with it.

**System**
    Piece of code to operate on data in components for a single frame.

Details
-------

ecs defines a few core core classes:

* ``Entity``
* ``Component``
* ``System``
* ``EntityManager``
* ``SystemManager``

The ``Entity`` class is simply a representation of a unique identifier, and is not to be subclassed. The ``Component`` class is intended to be subclassed for your custom components. ``System`` is also intended to be subclassed for your custom systems.

The ``EntityManager`` is a database that stores ``Component`` subclasses, referenced by their type and entity ID. The ``SystemManager`` maintains a set of ``System`` instances and allows them to perform their operations.

The real action happens in the ``update()`` method of your subclassed ``System`` classes. A ``System`` instance queries the ``EntityManager`` database for a set of ``Component`` subclasses and operates on the data contained in them.

Compatibility
-------------

ecs is compatible with CPython 2.6, 2.7, 3.3, and PyPy 2.2.0. CPython 3.0–3.2 may also work, but Python 3 users are encouraged to upgrade to Python 3.3. If upgrade is not a possibility for you, please file a issue! Tests ensuring compatibility are run continuously on Travis-CI_ and can also be run locally using tox_.

.. _Travis-CI: https://travis-ci.org/seanfisk/ecs
.. _tox: http://tox.readthedocs.org/en/latest/

Examples, Documentation, Contributions, and Issues
--------------------------------------------------

ecs is a very young project. As such, work on examples and documentation is just getting started. However, if you have read some of the articles mentioned on the `Entity Systems wiki`_, use of ecs should be quite clear. The codebase is quite small and simple and has a comprehensive set of tests to go with it. Those with questions of any sort are encouraged to `open an issue`_. Contributions are always welcome!

.. _open an issue: https://github.com/seanfisk/ecs/issues/new

Similar Projects
----------------

This module was written because current entity/component system implementations for Python are scarce or underdeveloped. Here are some other projects similar to this one:

* PyArtemis_, a seemingly unmaintained port of Artemis to Python
* Marcus von Appen's python-utils_, which include ebs_, an entity system framework similar to ``ecs``. However, ``ebs`` does not draw a distinction between *entity* and *component*, which we feel is significant.

.. _PyArtemis: https://github.com/kernhanda/PyArtemis
.. _python-utils: https://bitbucket.org/marcusva/python-utils
.. _ebs: http://python-utilities.readthedocs.org/en/latest/ebs.html

Further Reading
---------------

Entity/component systems are a relatively new concept. The canonical source for all entity system-related topics is the `Entity Systems wiki`_, created by Adam Martin. Adam Martin has also written abundantly in his `series of posts about Entity Systems`_, which are a great read for those just getting familiar with the concept.

.. _Entity Systems wiki: http://entity-systems.wikidot.com/es-approaches
.. _series of posts about Entity Systems: http://t-machine.org/index.php/2007/09/03/entity-systems-are-the-future-of-mmog-development-part-1/

History
-------

ecs was originally created by `Kevin Ward`_, and is now maintained by `Sean Fisk`_. I (Sean) am using ecs in a game written using the Panda3D_ game engine.

.. _Kevin Ward: https://github.com/wkevina
.. _Sean Fisk: https://github.com/seanfisk
.. _Panda3D: http://www.panda3d.org/
