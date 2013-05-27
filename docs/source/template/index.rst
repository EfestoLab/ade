Template system
===============

Ade base all its logic on top of a set of fragment folder, contained into a template path.
The template folder structure has to follow some simple rules:

structure
---------
Templates are contained into a top level folder defined by a template_path.

.. code-block:: bash

	.
	└── <template_folder>
		├── @+show+@
		├── @+department+@
		├── @+sequence+@
		├── @+shot+@
		├── @sandbox@
		├── etc....


.. toctree::
	:maxdepth: 1

	default/index.rst


