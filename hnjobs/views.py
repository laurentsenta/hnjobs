from . import app
from flask import render_template, jsonify, request, session, redirect, url_for
from jinja2 import evalcontextfilter, Markup, escape
import re

import json

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


with open("output.json", "r") as f:
    JSON = json.load(f)
    DATA = JSON[0]

def all_keywords(xs, exclude=[]):
    # all keywords
    k = xs['posts']
    k = map(lambda x: x['keywords'], k)
    k = map(set, k)
    k = reduce(lambda x, y: x | y, k)

    k -= set(exclude)

    return k

import copy

def filter_keyword(x, k):
    x = copy.deepcopy(x)
    x['posts'] = filter(lambda x: k in x['keywords'], x['posts'])
    return x

def add_filter(fs, f):
    fs = copy.deepcopy(fs)
    fs.append(f)
    fs = sorted(fs)
    return '+'.join(fs)

def remove_filter(fs, f):
    fs = copy.deepcopy(fs)
    fs.remove(f)
    fs = sorted(fs)
    return '+'.join(fs)

app.jinja_env.globals.update(add_filter=add_filter)
app.jinja_env.globals.update(remove_filter=remove_filter)


# http://flask.pocoo.org/snippets/28/
@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
        for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

@app.route('/') # does not work with frozen using defaults
def meh():
    return filtered('')

@app.route('/<path:filters>/')
#@app.route('/', defaults={'filters': ''})
def filtered(filters):

    print filters

    f = filters.split("+") if len(filters) > 0 else []
    data = reduce(lambda x, k: filter_keyword(x, k), f, DATA)

    ks = all_keywords(data, f)

    return render_template("home.html", date=data['date'], posts=data['posts'], keywords=ks, filter=f)

