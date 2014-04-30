import sys, os
import sphinx_rtd_theme

extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.doctest',
	'sphinx.ext.viewcode'
]

templates_path = ['_templates']

source_suffix = '.rst'
master_doc = 'index'

project = u'Ade'
copyright = u'2013, Lorenzo Angeli'

version = '0.1.0'
release = '0.1.0'
exclude_patterns = []

pygments_style = 'sphinx'

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['_static']
htmlhelp_basename = 'Adedoc'
latex_elements = {
}

latex_documents = [
  ('index', 'Ade.tex', u'Ade Documentation',
   u'Lorenzo Angeli', 'manual'),
]

man_pages = [
    ('index', 'ade', u'Ade Documentation',
     [u'Lorenzo Angeli'], 1)
]

texinfo_documents = [
  ('index', 'Ade', u'Ade Documentation',
   u'Lorenzo Angeli', 'Ade', 'Templated file system manager.',
   ''),
]
