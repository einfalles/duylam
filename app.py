# -*- coding: utf-8 -*-

import os

from flask import Flask, render_template
from flask_script import Manager
from flask_frozen import Freezer
from flask_assets import Environment, Bundle, ManageAssets
# from flask_flatpages import FlatPages
from lib.mdjinja import MarkdownJinja
from lib.flatpages import FlatPages


#
# Config
#
app = Flask(__name__, static_folder="assets")
app.config.from_pyfile('settings.py')


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

css_lib_files = ['normalize.css']
css_lib = Bundle(*['lib/css/' + file for file in css_lib_files],
                 filters='cleancss', output='gen/css_lib.css')
assets.register("css_lib", css_lib)

js_lib_files = ['jquery.js']
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
    years = {
        3008: [],
        2017: [],
        2016: [],
        2015: [],
        2014: [],
        2013: [],
        2011: [],
        2010: [],
        2009: []
    }
    all_pages = pages.get_all()
    for page in all_pages:
        key_year = all_pages[page].meta['date'].year
        years[key_year].append(all_pages[page])
    for k,v in years.items():
        sorted_posts = sorted(v, reverse=True,key=lambda post: post.meta['date'])
        years[k] = sorted_posts

    return render_template("allpages.jinja", years=years)

# @app.route('/portfolio')
# def view_portfolio():
#     return "This is my portfolio"
#
# @app.route('/dispatch')
# def view_dispatch():
#     return "These are my notes"
#
# @app.route('/about')
# def view_about():
#     return "This will be a sort of manifesto"
#
# @app.route('/project/<path:path>/')
# def page(path):
#     page = pages.get_or_404(path)
#     return render_template('page.jinja', page=page)


#
# livereload infra
#
from livereload import Server, shell
from formic import FileSet

def make_livereload_server(wsgi_app):
    server = Server(wsgi_app)
    build_cmd = "true"
    print("Files being monitored:")
    cwd = os.getcwd()
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
