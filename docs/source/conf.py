import os
import sys

# Путь к корневой директории проекта
sys.path.insert(0, os.path.abspath("../.."))

project = 'Api OpenWeatherMap'
copyright = '2026, Kristina Pachi'
author = 'Kristina Pachi'
release = '1.0'

extensions = [
    'sphinx.ext.autodoc',  # Автоматическое извлечение docstrings
    'sphinx.ext.napoleon',  # Поддержка Google/NumPy стилей (не мешает reST)
    'sphinx.ext.viewcode',  # Показывать исходный код в документации
    'sphinx.ext.todo',  # Поддержка TODO
]

templates_path = ['_templates']

exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
]

language = 'ru'

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
