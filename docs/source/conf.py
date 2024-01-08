# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

from typing import Any

project: str = "OpenSearch Python Client"
copyright: str = "OpenSearch Project Contributors"
author: str = "OpenSearch Project Contributors"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions: Any = [
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
    "sphinx.ext.viewcode",
    "myst_parser",  # https://myst-parser.readthedocs.io/
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",  # https://github.com/executablebooks/sphinx-copybutton
    "sphinx.ext.todo",  # https://www.sphinx-doc.org/en/master/usage/extensions/todo.html
]

# Add any paths that contain templates here, relative to this directory.
templates_path: Any = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: Any = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme: str = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path: Any = ["_static"]

# -- additional settings -------------------------------------------------
intersphinx_mapping: Any = {
    "python": ("https://docs.python.org/3", None),
}

html_logo: str = "imgs/OpenSearch.svg"

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files: Any = [
    "css/custom.css",
]

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx: bool = False

# add github link
html_context: Any = {
    "display_github": True,
    "github_user": "opensearch-project",
    "github_repo": "opensearch-py",
    "github_version": "main/docs/source/",
}

# -- autodoc config -------------------------------------------------
# This value controls how to represent typehints.
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autodoc_typehints
autodoc_typehints: str = "description"

# This value selects what content will be inserted into the main body of an autoclass directive.
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autoclass_content
autoclass_content: str = "both"

# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-add_module_names
# add_module_names = False

# The default options for autodoc directives.
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autodoc_default_options
autodoc_default_options: Any = {
    # If set, autodoc will generate document for the members of the target module, class or exception.  # noqa: E501
    # https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-option-automodule-members
    "members": True,
    "show-inheritance": True,
    # If set, autodoc will also generate document for the special members (that is, those named like __special__).  # noqa: E501
    # https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-option-automodule-special-members
    "special-members": None,
    # If set, autodoc will also generate document for the private members (that is, those named like _private or __private).  # noqa: E501
    # https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-option-automodule-private-members
    "private-members": None,
    "exclude-members": "__weakref__, __init__",
}
