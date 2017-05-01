#!/usr/bin/env python

AUTHOR = 'Pybonacci'
SITENAME = 'Pybonacci'
SITESUBTITLE = u'Blog sobre Python científico en español'
SITEURL = ''
PATH = 'content'
TIMEZONE = 'Europe/Madrid'
DEFAULT_LANG = 'es'
LOCALE = 'es_ES.UTF-8'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Set the article URL
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

#MARKUP = ('md', 'ipynb')
#PLUGINS = ['ipynb.markup']

MARKUP = ['md']
PLUGIN_PATHS = ['./plugins', './plugins/pelican-plugins']
PLUGINS = [
    'summary',       # auto-summarizing articles
    'feed_summary',  # use summaries for RSS, not full articles
    'ipynb.liquid',  # for embedding notebooks
    'liquid_tags.img',  # embedding images
    'liquid_tags.video',  # embedding videos
    'liquid_tags.include_code',  # including code blocks
    'liquid_tags.literal'
]
IGNORE_FILES = ['.ipynb_checkpoints']

# for liquid tags
CODE_DIR = 'downloads/code'
NOTEBOOK_DIR = 'downloads/notebooks'

# THEME SETTINGS
THEME = './theme/'

ABOUT_PAGE = '/pages/acerca-de-pybonacci.html'
TWITTER_USERNAME = 'Pybonacci'
GITHUB_USERNAME = 'Pybonacci'
SHOW_ARCHIVES = True
SHOW_FEED = False  # Need to address large feeds

ISSO_HOST = 'localhost:1234'

ENABLE_MATHJAX = True

STATIC_PATHS = ['images', 'figures', 'videos', 'downloads', 'favicon.ico']

# Footer info

LICENSE_URL = "https://github.com/Juanlu001/pybonacci.github.io-source/blob/master/LICENSE"
LICENSE = "MIT"
