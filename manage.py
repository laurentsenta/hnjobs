from hnjobs import app
from flask_debugtoolbar import DebugToolbarExtension

from flask.ext.script import Manager

manager = Manager(app)

if __name__ == '__main__':
    app.debug = True
    toolbar = DebugToolbarExtension(app)
    manager.run()

