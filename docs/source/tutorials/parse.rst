Parse
=====

Parse the given path:
---------------------

.. code-block:: bash

    $ ade parse --path /tmp/white/job/AF/AF001/sandbox/username/maya/
    >> {"department": "job", "show": "white", "shot": "AF001", "user": "username", "sequence": "AF"}


Parse the current path:
-----------------------

.. code-block:: bash

    $ cd /tmp/white/job/AF/AF001/sandbox/username/maya/
    $ ade parse
    >> {"department": "job", "show": "white", "shot": "AF001", "user": "username", "sequence": "AF"}
