Create
======

.. note::
    - path is set to ./ by default

Initialise a new show into a custom path:
-------------------------------------------

.. code-block:: bash

    $ ade create --data show=white --verbose debug --path /jobs --template @+show+@

Create a shot folder into the home directory of the user:
---------------------------------------------------------

.. code-block:: bash

    $ ade create --data show=white department=dev sequence=AA shot=AA001 --template @+shot+@ --verbose debug --path $HOME


Create a sandbox folder into the current folder:
------------------------------------------------

.. code-block:: bash

    $ ade create --template @sandbox@




