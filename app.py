# -*- coding: utf-8 -*-

import os
import random

from flask import request
from flask import Flask, render_template
from flask_script import Manager
from flask_frozen import Freezer
from flask_assets import Environment, Bundle, ManageAssets
from flask_flatpages import FlatPages
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

css_files = ['home.less','atoms.less','molecules.less','organisms.less']
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

js_lib_files = ['vue.js']
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
# Utilities
#
def project_sort(all_pages):
    years = {
        2000: [], 2017: [], 2016: [], 2015: [],
        2014: [], 2013: [], 2011: [], 2010: [],
        2009: []
    }
    for page in all_pages:
        key_year = all_pages[page].meta['date'].year
        years[key_year].append(all_pages[page])
    years.pop(2000)
    for k,v in years.items():
        sorted_posts = sorted(v, reverse=True,key=lambda post: post.meta['date'])
        years[k] = sorted_posts
    return years
#
# Routes
#
@app.route('/')
def index():
    koan = "Welcome."
    all_pages = pages.get_all()
    years = project_sort(all_pages)
    return render_template("allpages.jinja", years=years, koan=koan,request=request)

@app.route('/portfolio')
def view_portfolio():
    projects = ['siempo','latch','walkback','jiffy','sunsama','tunesmash']
    portfolio_pages = []
    for project in projects:
        portfolio_pages.append(pages.get_or_404(project))
    return render_template('portfolio.jinja',projects=portfolio_pages)

@app.route('/dispatch')
def view_dispatch():
    return render_template('dispatch.jinja')

@app.route('/about')
def view_about():
    page = pages.get_or_404('about')
    return render_template('page.jinja', pages=page)


@app.route('/project/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    all_pages = pages.get_all()
    all_pages_index = []
    page_index = 0
    next_index = 0
    prev_index = 0
    all_pages = project_sort(all_pages)
    for year in all_pages:
        all_pages_index = all_pages_index + all_pages[year]
    page_index = all_pages_index.index(page)
    prev_index = (page_index - 1) % len(all_pages_index)
    next_index = (page_index + 1) % len(all_pages_index)
    page_prev = all_pages_index[prev_index]
    page_next = all_pages_index[next_index]
    return render_template('page.jinja', pages=page, next=random.choice(all_pages_index).path, page_prev=page_prev.path, page_next=page_next.path)


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
    freezer.register_generator(index)
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
