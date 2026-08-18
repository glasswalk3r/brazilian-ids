# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from pathlib import Path


def release_from_project():
    try:
        import tomllib
    except ModuleNotFoundError:  # Python < 3.11
        import tomli as tomllib

    sys.path.insert(0, os.path.join(os.path.abspath(os.path.join("..", "..")), "src"))

    pyproject_file = Path(__file__).resolve().parents[2] / "pyproject.toml"

    with pyproject_file.open("rb") as _fh:
        pyproject = tomllib.load(_fh)

    return pyproject["project"]["version"]


project = "brazilian-ids"
copyright = "2024, Alceu Rodrigues de Freitas Junior"
author = "Alceu Rodrigues de Freitas Junior"
release = release_from_project()

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
]

exclude_patterns: list[str] = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "private-members": False,
    "special-members": False,
}
autodoc_typehints = "description"

html_static_path = ["_static"]
