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

#SUMMARY_USE_FIRST_PARAGRAPH = True
SUMMARY_MAX_LENGTH = 140

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
    'liquid_tags.youtube',  # embedding youtube videos
    'liquid_tags.include_code',  # including code blocks
    'liquid_tags.literal',
    #'footer_insert',  # https://github.com/getpelican/pelican-plugins/tree/master/footer_insert
    #'headerid',  # https://github.com/getpelican/pelican-plugins/tree/master/headerid
    #'gravatar',  # https://github.com/getpelican/pelican-plugins/tree/master/gravatar
    #'autopages',  # https://github.com/getpelican/pelican-plugins/tree/master/autopages
    #'simple_footnotes', # https://github.com/getpelican/pelican-plugins/tree/master/simple_footnotes
    #'show_source',  # https://github.com/getpelican/pelican-plugins/tree/master/show_source
    #'series',  # https://github.com/getpelican/pelican-plugins/tree/master/series
    #'representative_image',  # https://github.com/getpelican/pelican-plugins/tree/master/representative_image
]
IGNORE_FILES = ['.ipynb_checkpoints']

# for liquid tags
CODE_DIR = 'downloads/code'
NOTEBOOK_DIR = 'downloads/notebooks'

# THEME SETTINGS
THEME = './theme/'

ABOUT_PAGE = '/pages/acerca-de-pybonacci.html'
CONTRIBUTING_PAGE = '/pages/como-contribuir.html'
TWITTER_USERNAME = 'Pybonacci'
GITHUB_USERNAME = 'Pybonacci'
SHOW_ARCHIVES = True
SHOW_FEED = False  # Need to address large feeds

ISSO_HOST = 'https://pybocomments.runbear.webfactional.com'

ENABLE_MATHJAX = True

STATIC_PATHS = ['images', 'figures', 'videos', 'downloads', 'favicon.ico', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'}}

# Footer info
LICENSE_URL = "https://github.com/Pybonacci/pybonacci.github.io/blob/sources/LICENSE.md"
LICENSE_NAME = "CC BY-SA 4.0 + MIT"
