from flask import Blueprint, render_template, redirect, url_for, flash, session

from app import app
# from global_vars import logger

from auth.models import User
from .models import Player
# from .models import GameSession
# from .forms import GameSessionForm


from .mud.user import User as GameUser


from .gamego.signals import sig_init
# from .talker import talker


mudexe = Blueprint('mudexe', __name__)


@mudexe.route("/start/<username>")
def start_game(username):
    """
    Render start page
    """
    sig_init()
    game_user = GameUser(username)
    user = game_user.model
    app.logger.info("GAME ENTRY: %s[%s]", user.fullname, user.uid)
    try:
        game_user.prepare_game()
    except Exception as e:
        flash(e)
    session["user_id"] = user.id

    # for i in range(5):
    #     do_signal(SIGALRM, user)
    # do_signal(SIGTERM, user)
    return render_template(
        'mudexe/view.html',
        title="Sessions",
        user=game_user,
        users=User.query.all(),
        players=Player.query.all(),
        user_id=session["user_id"],
    )


@mudexe.route("/play")
def play_game():
    """
    Render game page
    """
    user_id = session["user_id"]
    user = User.query.get(user_id)
    if user is None:
        return redirect(url_for("mudexe.start_game", username="User"))

    game_user = GameUser(user.username)
    user = game_user.model
    return render_template(
        'mudexe/view.html',
        title="Sessions",
        user=game_user,
        users=User.query.all(),
        players=Player.query.all(),
        user_id=session["user_id"],
    )
