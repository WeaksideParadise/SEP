# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


import os
import sys
# add code path to 
codePath = os.path.abspath('../../Meilenstein_2/')

sys.path.insert(0,codePath)

project = 'Ressource Manager'
copyright = '2024, Markus Meier, Tom Seidel, Robert Landgraf, Wael Azran, Marc Blechschmidt, Kasem'
author = 'Markus Meier, Tom Seidel, Robert Landgraf, Wael Azran, Marc Blechschmidt, Kasem'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

# Optionally, you can enable autosummary to automatically generate stub files
autosummary_generate = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'de'

# Add this line to include private members
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': True,  # Include private members like _connect and _setup
    'show-inheritance': True,
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
