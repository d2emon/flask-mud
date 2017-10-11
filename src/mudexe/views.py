from flask import Blueprint, render_template, redirect, url_for, flash, session
from datetime import datetime

from app import app
# from global_vars import logger

from auth.models import User
from .models import Player
# from .models import GameSession
# from .forms import GameSessionForm


from .mud.user import User as GameUser
from .mud.tty import PageTerminal


from .gamego.signals import sig_init, do_signal, SIGALRM


mudexe = Blueprint('mudexe', __name__)


@mudexe.route("/start/<username>")
def start_game(username):
    """
    Render start page
    """
    sig_init()

    user_id = session.get("user_id", 0)
    if user_id:
        return redirect(url_for("mudexe.play_game"))

    game_user = GameUser(username)
    user = game_user.model
    app.logger.info("GAME ENTRY: %s[%s]", user.fullname, user.uid)
    try:
        game_user.prepare_game()
    except Exception as e:
        flash(e)
    session["user_id"] = user.id

    return render_template(
        'mudexe/start.html',
        title="Entering Game",
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
    user_id = session.get("user_id", 0)
    user = User.query.get(user_id)
    if user is None:
        return redirect(url_for("mudexe.start_game", username="User"))


    sig_init()
    game_user = GameUser(user.username)
    if not game_user.load():
        session["user_id"] = 0
        return redirect(url_for("mudexe.start_game", username="User"))


    terminal = PageTerminal("MUD_PROGRAM_NAME", user.username)
    terminal.set_user(game_user)


    # Get last active
    last_active = session.get("last_active")
    if not last_active:
        last_active = datetime.now()
        session["last_active"] = last_active
    timeleft = datetime.now() - last_active
    if timeleft.seconds > 2:
        time_to_turn = True
        session["last_active"] = datetime.now()
    else:
        time_to_turn = False

    if time_to_turn:
        do_signal(SIGALRM, terminal)

    room_text = game_user.look()

    terminal.on_text("test text")
    answer = terminal.text

    terminal.text = ""
    terminal.do_loop()

    # do_signal(SIGTERM, terminal)
    return render_template(
        'mudexe/view.html',
        title=terminal.title,
        debug=game_user.debug_mode,
        user=game_user,
        room=game_user.room,

        room_text=room_text,

        users=User.query.all(),
        players=Player.query.all(),
        user_id=session["user_id"],

        terminal=terminal,
        prompt=terminal.prmpt,
        text1=answer,
        text=terminal.text,
        time_to_turn=time_to_turn,
    )
