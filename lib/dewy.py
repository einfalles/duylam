# -*- coding: utf-8 -*-
"""
dewy -- forked version of flask_flatpages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

dewy is a collection of greate utitilies.

The code is small enough, so we're just going to fork and customize as
necessary over time.

:copyright: (c) 2018 by Duylam
:license: BSD, see LICENSE for more details.
"""

import feedparser

def rename_files():
    directory = '/Users/rachelgoree/development/portfolio/duylam/templates'
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            if filename.find('.jinja') > 0:
                subdirectoryPath = os.path.relpath(subdir, directory) #get the path to your subdirectory
                filePath = os.path.join(subdirectoryPath, filename) #get the path to your file
                newFilePath = filePath.replace(".jinja",".jinja2.html") #create the new name

def project_sort(all_pages):
    years = {
        2000: [],
        2017: [],
        2016: [],
        2015: [],
        2014: [],
        2013: [],
        2011: [],
        2010: [],
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

def arena_pull():
    url = "https://www.are.na/duylam-nguyen-ngo/dispatch-1525473726/feed/rss"
    feed = feedparser.parse(url)['entries']
    return feed
