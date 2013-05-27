
Examples
========
Here some simple examples on how use ade:


Create a shot folder into the home directory of the user:
---------------------------------------------------------

.. code-block:: bash

 	$ ade create --data show=white department=dev sequence=AA shot=AA001 --template @+shot+@ --verbose debug --mount_point $HOME


Initialise a new show into a custom path:
-------------------------------------------

.. note::
	mount_point is set to /tmp by default

.. code-block:: bash

 	$ ade create --data show=white --verbose debug --mount_point /jobs --template @+show+@


Create a sandbox folder into the current folder:
------------------------------------------------

.. code-block:: bash

 	$ ade create --mount_point ./ --template @sandbox@  --verbose debug


Parse the given path:
---------------------

.. code-block:: bash

 	$ ade parse --path /tmp/white/job/AF/AF001/sandbox/username/maya/ 
	>> {"department": "job", "show": "white", "shot": "AF001", "user": "username", "sequence": "AF"}


Parse the current path:
---------------------

.. code-block:: bash

	$ cd /tmp/white/job/AF/AF001/sandbox/username/maya/
 	$ ade parse
	>> {"department": "job", "show": "white", "shot": "AF001", "user": "username", "sequence": "AF"}




