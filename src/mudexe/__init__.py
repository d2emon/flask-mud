from flask_script import Manager


from .models import *
from .views import mudexe as mudexe_blueprint
from .commands import manager as mudexe_manager
from global_vars import set_logger


# __version__ = '3.3.7.1.dev1'


class MudExe(object):
    def __init__(self, app=None, **kwargs):
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        manager = kwargs.get('manager')

        app.register_blueprint(mudexe_blueprint, url_prefix='/mud/exe')

        set_logger(app.logger)

        if manager is None:
            manager = Manager(usage="Main application")
        manager.add_command("play", mudexe_manager)
