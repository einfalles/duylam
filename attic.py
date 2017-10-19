import os
from os import getcwd
from flask import Flask, render_template

# ~~~~~~
# NOT SURE IF THIS IS NECESSARY ANYMORE
from flask_script import Manager

"""
Freezer is the manager for Frozen Flask. Your Freezer instance will create the
static files, directories, etc
"""
from flask_frozen import Freezer

"""
These are used to managed all the assets via Flask-Assets. Environment is
basically a bin. Bundle are folders. Your css, js, etc assets are put into a
Bundle, and 'registered' with the Environment. We might not need ManageAssets
"""
from flask_assets import Environment, Bundle, ManageAssets
# from lib.flatpages import FlatPages
from flask_flatpages import FlatPages
from lib.mdjinja import MarkdownJinja

#
# Config
#

DEBUG = True

# Use Markdown for simple pages/content
APP_DIR = os.path.dirname(os.path.abspath(__file__))
def parent_dir(path):
    '''Return the parent of a directory.'''
    return os.path.abspath(os.path.join(path, os.pardir))
PROJECT_ROOT = parent_dir(APP_DIR)
# In order to deploy to Github pages, you must build the static files to
# the project root
FREEZER_DESTINATION = PROJECT_ROOT
FREEZER_BASE_URL = "http://localhost/"
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_ROOT = os.path.join(APP_DIR, 'pages')
FLATPAGES_EXTENSION = '.md'

# FREEZER_BASE_URL = "http://localhost/"
FREEZER_RELATIVE_URLS = False

ASSETS_DEBUG = DEBUG

app = Flask(__name__, static_folder="assets")

# LOAD CONFIGURATION FILE. I THINK THIS INSTANCE MEANS LOAD IT FROM APP.PY
app.config.from_object(__name__)

#
# Jinja, CSS, LESS, and JS Assets
#
WATCH_PATTERNS = (
    "README.md",
    "/templates/**",
    "/pages/**",
    "/assets/**"
)

assets = Environment(app)

css_files = ['home.less']
css_all = Bundle(*['less/' + file for file in css_files],
                 filters=['less', 'cleancss'], output='gen/css_all.css')
assets.register("css_all", css_all)

js_files = ['home.js']
js_all = Bundle(*['js/' + file for file in js_files],
                filters='rjsmin', output='gen/js_all.js')
assets.register("js_all", js_all)

css_lib_files = ['bootstrap.css', 'bootstrap-theme.css']
css_lib = Bundle(*['lib/css/' + file for file in css_lib_files],
                 filters='cleancss', output='gen/css_lib.css')
assets.register("css_lib", css_lib)

js_lib_files = ['jquery.js', 'underscore.js', 'bootstrap.js', 'd3.js']
js_lib = Bundle(*['lib/js/' + file for file in js_lib_files],
                filters='rjsmin', output='gen/js_lib.js')
assets.register("js_lib", js_lib)

#
# Plugins
#

freezer = Freezer(app)
pages = FlatPages(app)
md = MarkdownJinja(app)
manager = Manager(app)
manager.add_command("assets", ManageAssets(assets))

#
# Routes
#


@app.route('/')
def index():
    page = pages.get("index")
    print(page)
    return render_template("page.jinja", page=page)


@app.route('/list/')
def list():
    return render_template("allpages.jinja", pages=pages)


@app.route('/pages/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.jinja', page=page)

@freezer.register_generator
def page():
    yield {'path': 'index.md'}
    # yield {'path': 'markdown.md'}
    # yield {'path': 'markdown.md'}

# @app.route('/tag/<string:tag>/')
# def tag(tag):
#     tagged = [p for p in pages if tag in p.meta.get('tags', [])]
#     return render_template('alltags.jinja', pages=tagged, tag=tag)


#
# livereload infra
#


from livereload import Server, shell
from formic import FileSet



def make_livereload_server(wsgi_app):
    server = Server(wsgi_app)

    # XXX: build step could be useful, e.g.
    # making it `python app.py build`, but
    # in this use case not really necessary
    build_cmd = "true"

    print("Files being monitored:")

    cwd = getcwd()

    for pattern in WATCH_PATTERNS:
        print( "Pattern: {0}".format(pattern))
        for filepath in FileSet(include=pattern):
            print("=> {0}".format(os.path.relpath(filepath, cwd)))
            server.watch(filepath, build_cmd)
        print

    return server


#
# Commands
#


@manager.command
def build():
    """Creates a static version of site in ./build."""
    app.debug = True
    app.testing = True

    freezer.freeze()


@manager.command
def livereload():
    """Runs the Flask development server under livereload."""
    # wire livereload to Flask via wsgi
    flask_wsgi_app = app.wsgi_app
    server = make_livereload_server(flask_wsgi_app)
    # serve application
    server.serve(host='127.0.0.1', port=5000)


if __name__ == "__main__":
    manager.run()
    # freezer.run(debug=True)
