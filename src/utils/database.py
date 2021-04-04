from flask_sqlalchemy import SQLAlchemy
from utils.create_app import app
from configs import Settings


def create_database(app):
    try:
        db = SQLAlchemy(app)
    except (RuntimeError, ValueError, TypeError, BaseException) as e:
        return e.name

    return db


mlbdb = create_database(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}/{}".format(Settings.SECRETS['MLB_DATABASE_USER'],
                                                                          Settings.SECRETS['MLB_DATABASE_PASSWORD'],
                                                                          Settings.SECRETS['MLB_DATABASE_HOST'],
                                                                          Settings.SECRETS['MLB_DATABASE_DB'])
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = { "pool_recycle": 1800 }
mlbdb.database.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                             app.config['SQLALCHEMY_ENGINE_OPTIONS'])


ncaambdb = create_database(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}/{}".format(Settings.SECRETS['NCAAMB_DATABASE_USER'],
                                                                          Settings.SECRETS['NCAAMB_DATABASE_PASSWORD'],
                                                                          Settings.SECRETS['NCAAMB_DATABASE_HOST'],
                                                                          Settings.SECRETS['NCAAMB_DATABASE_DB'])
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = { "pool_recycle": 1800 }
ncaambdb.database.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                             app.config['SQLALCHEMY_ENGINE_OPTIONS'])

nfldb = create_database(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}/{}".format(Settings.SECRETS['NFL_DATABASE_USER'],
                                                                          Settings.SECRETS['NFL_DATABASE_PASSWORD'],
                                                                          Settings.SECRETS['NFL_DATABASE_HOST'],
                                                                          Settings.SECRETS['NFL_DATABASE_DB'])
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = { "pool_recycle": 1800 }
nfldb.database.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                             app.config['SQLALCHEMY_ENGINE_OPTIONS'])