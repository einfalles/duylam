# -*- coding: utf-8 -*-

# import os
#
# def parent_dir(path):
#     '''Return the parent of a directory.'''
#     print(os.path.abspath(os.path.join(path, os.pardir)))
#     return os.path.abspath(os.path.join(path, os.pardir))
#
# REPO_NAME = ""
# DEBUG = True

# APP_DIR = os.path.dirname(os.path.abspath(__file__))

# PROJECT_ROOT = parent_dir(APP_DIR)
# PROJECT_ROOT = APP_DIR
# In order to deploy to Github pages, you must build the static files to
# the project root
# FREEZER_DESTINATION = PROJECT_ROOT
# Since this is a repo page (not a Github user page),
# we need to set the BASE_URL to the correct url as per GH Pages' standards
# FREEZER_BASE_URL = "http://localhost/{0}".format(REPO_NAME)

# FREEZER_REMOVE_EXTRA_FILES = False  # IMPORTANT: If this is True, all app files
                                    # will be deleted when you run the freezer
# FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite']
# FLATPAGES_AUTO_RELOAD = DEBUG
# FLATPAGES_ROOT = os.path.join(APP_DIR, 'pages')
# FLATPAGES_EXTENSION = '.md'
FREEZER_IGNORE_MIMETYPE_WARNINGS = True
DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FREEZER_RELATIVE_URLS = True
FREEZER_DESTINATION = 'docs'
# ASSETS_DEBUG = DEBUG
