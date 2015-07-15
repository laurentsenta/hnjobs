from . import app

from flask import render_template, jsonify, request, session, redirect, url_for
from jinja2 import evalcontextfilter, Markup, escape

import re
import json
import copy

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


# Load the last scraping
with open("output.json", "r") as f:
    JSON = json.load(f)
    DATA = JSON[0]

# DATA is represented as:
# {
#  date: "Month Year",
#  posts: [
#           {
#            text: 'text for post 1',
#            keywords: ['keyword', 'for', 'post 1']
#           },
#           ...
#         ]
#  url: hn post url
#  }


# Data Manipulation
# =================

def filter_keyword(x, k):
    """
    Keep only posts containing the keyword K
    """
    x = copy.deepcopy(x)
    x['posts'] = filter(lambda x: k in x['keywords'], x['posts'])
    return x

def all_keywords(xs, exclude=[]):
    """
    List all keywords in the current data XS
    """
    # all keywords
    k = xs['posts']
    k = map(lambda x: x['keywords'], k)
    k = map(set, k)
    k = reduce(lambda x, y: x | y, k)

    k -= set(exclude)

    return k


# Jinja Functions
# ===============

def add_filter(fs, f):
    """
    Add the keyword F to the list FS,
    Return the filter path "f1+f2+...+fn"
    """
    fs = copy.deepcopy(fs)

    if f not in fs:
        fs.append(f)

    fs = sorted(fs)
    return '+'.join(fs)

def remove_filter(fs, f):
    """
    Remove the keyword F from the list FS,
    Return the filter path "f1+f2+...+fn"
    """
    fs = copy.deepcopy(fs)

    if f in fs:
        fs.remove(f)

    fs = sorted(fs)
    return '+'.join(fs)

app.jinja_env.globals.update(add_filter=add_filter)
app.jinja_env.globals.update(remove_filter=remove_filter)

# http://flask.pocoo.org/snippets/28/
@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    """
    Add paragraph and line return
    """
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
        for p in _paragraph_re.split(value))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


# Views
# =====

@app.route('/') # Else frozen flask does not load the default filter
def meh():
    return filtered('')

#@app.route('/', defaults={'filters': ''})
@app.route('/<path:filters>/')
def filtered(filters):
    # The list of keywords
    f = filters.split("+") if len(filters) > 0 else []

    # Filter the data using the keywords
    data = reduce(lambda x, k: filter_keyword(x, k), f, DATA)

    # List all the remaining keywords
    ks = all_keywords(data, f)

    return render_template("home.html",
            date=data['date'],
            posts=data['posts'],
            keywords=ks,
            filter=f,
            url=data['url'])

