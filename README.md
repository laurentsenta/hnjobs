HNJobs
======

A single view visualisation for Hacker News Who Is Hiring Posts.

It's online at [hnjobs.lsenta.io](http://hnjobs.lsenta.io).

The data (`output.json`) comes from a simple
[web-scraping script](https://github.com/lsenta/pow/blob/master/who-is-hiring-2015/hiring-2.ipynb)

Usage
-----

- Run `python manage.py runserver` to run the local dev server
- Run `python freezer.py` to generate the static site in `hnjobs/static/build/`
