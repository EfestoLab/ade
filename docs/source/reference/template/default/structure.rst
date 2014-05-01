Default
#######

.. note::
    Ade contains a default template structure, built to build and handle a vfx
    project structures.


Context folders:
================

A collection of high level context folder definition.

show
----
Usually the root of the poject.

Contains references to:

 * config
 * department
 * temp

.. note::
    The config folder contains a file placeholder.
    where some project related configs are supposed to be stored.

.. code-block:: bash

    ├── @+show+@
    │   ├── @config@
    │   │   └── setup.json
    │   ├── @+department+@
    │   ├── editorial
    │   ├── references
    │   ├── @temp@
    │   └── vault

department
----------

Define membership of department we are working into.

Contains reference to :

* config
* sequence

.. code-block:: bash

    ├── @+department+@
    │   ├── @config@
    │   └── @+sequence+@


sequence
--------

Define a sequence in the show

Contains reference to :

* config
* shot

.. code-block:: bash

    ├── @+sequence+@
    │   ├── @config@
    │   └── @+shot+@

shot
-----

Define a shot in the sequence

Contains reference to :

* config
* maya
* nuke
* sandbox

.. code-block:: bash

    ├── @+shot+@
    │   ├── build
    │   ├── @config@
    │   ├── @maya@
    │   ├── @nuke@
    │   └── @sandbox@

Applications folders:
=====================

maya
----

Contains the default maya structure with the workspace.mel file included

.. code-block:: bash

    ├── @maya@
    │   ├── images
    │   ├── particles
    │   ├── playblast
    │   ├── python
    │   │   └── +python_version+
    │   ├── scene
    │   ├── scripts
    │   ├── textures
    │   └── workspace.mel

nuke
----

Contains the simple nuke project folder

.. code-block:: bash

    ├── @nuke@
    │   └── scripts


Common Folders:
===============
Contain a set of common folder used all over the structure.

config
------

Contains a standard config folder .
Contain a set of configuration files for environments.

.. code-block:: bash

    ├── @config@
    │   └── envs
    │       └── software.json

sandbox
-------

.. code-block:: bash

    ├── @sandbox@
    │   └── +user+
    │       ├── @config@
    │       ├── @maya@
    │       ├── @nuke@
    │       └── @temp@

temp
----

.. code-block:: bash

    └── @temp@
        └── cache


