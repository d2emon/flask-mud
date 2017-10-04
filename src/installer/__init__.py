from flask_script import Manager


# from .models import *
# from .views import rpg as rpg_blueprint
from .commands import manager as install_manager


# __version__ = '3.3.7.1.dev1'


class Installer(object):
    def __init__(self, app=None, manager=None):
        if app is not None:
            self.init_app(app, manager)

    def init_app(self, app, manager=None):
        # app.static_folder = app.config.get('STATIC_FOLDER', 'static')
        # app.template_folder = app.config.get('TEMPLATE_FOLDER', 'templates')

        # self.logging = RotatingFileLogging(app)
        # self.toolbar = DebugToolbarExtension(app)
        pass
        # app.register_blueprint(pathfinder_blueprint, url_prefix='/pathfinder')
        # app.register_blueprint(gurps_blueprint, url_prefix='/gurps')
        # app.register_blueprint(tnt_blueprint, url_prefix='/tnt')

        if manager is None:
            manager = Manager(usage="Application Installer")
        manager.add_command("install", install_manager)
