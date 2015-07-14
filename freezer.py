from flask.ext.frozen import Freezer
from hnjobs import app

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()

