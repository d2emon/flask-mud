from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cache import Cache
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_script import Manager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_utils import FlaskUtils
from config import app_config

import os


# Env vars
debug = os.environ.get('FLASK_DEBUG', False)
config_name = os.environ.get('FLASK_CONFIG', 'production')


def create_app(debug=False, config_name='production'):
    app = Flask(__name__, instance_relative_config=True)

    # Loading config
    app.config.from_object(app_config.get(config_name))
    app.config.from_pyfile('config.py')
    if os.environ.get('FLASK_CONFIG_FILE', False):
        app.config.from_envvar('FLASK_CONFIG_FILE')
    print(app.config)
    return app


app = create_app(config_name=config_name)

# Loading modules
bootstrap = Bootstrap(app)

cache = Cache(app)

utils = FlaskUtils(app)

login_manager = LoginManager(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.login"

manager = Manager(app)

db = SQLAlchemy(app)
db.create_all()

migrate = Migrate(app, db)

session = Session(app)

# Importing blueprints
from auth import *
app.register_blueprint(auth_blueprint)
# app.register_blueprint(auth_blueprint, url_prefix='/auth')

# Something
from installer import *
installer = Installer(app, manager=manager, logging=utils.logging)

from mudexe import *
mudexe = MudExe(app, manager=manager, logging=utils.logging)

from app.views import *

# Adding commands from managers
# from auth.commands import manager as auth_manager
# from admin.commands import manager as admin_manager
# manager.add_command("user", auth_manager)
# manager.add_command("admin", admin_manager)
