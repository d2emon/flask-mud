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
from .mud.exceptions import GoError


from .gamego.signals import sig_init, do_signal, SIGALRM


mudexe = Blueprint('mudexe', __name__)


EXITS = {
    "north": 0,
    "east": 1,
    "south": 2,
    "west": 3,
    "up": 4,
    "down": 5,
    "n": 0,
    "e": 1,
    "s": 2,
    "w": 3,
    "u": 4,
    "d": 5,
}


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


def load_user():
    user_id = session.get("user_id", 0)
    user = User.query.get(user_id)
    if user is None:
        session["user_id"] = 0
        return None
    game_user = GameUser(user.username)
    if not game_user.load():
        session["user_id"] = 0
        return None
    return game_user


@mudexe.route("/play")
def play_game():
    """
    Render game page
    """
    user = load_user()
    if user is None:
        return redirect(url_for("mudexe.start_game", username="User"))

    sig_init()

    terminal = PageTerminal("MUD_PROGRAM_NAME", user.name)
    terminal.set_user(user)

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

    room_text = user.look()

    terminal.on_text("test text")
    answer = terminal.text

    terminal.text = ""
    terminal.do_loop()

    # do_signal(SIGTERM, terminal)
    return render_template(
        'mudexe/view.html',
        title=terminal.title,
        debug=user.debug_mode,
        user=user,
        room=user.room,

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


@mudexe.route("/go")
@mudexe.route("/go/<direction>")
def go(direction=""):
    """
    Render game page
    """
    user = load_user()
    if user is None:
        return redirect(url_for("mudexe.start_game", username="User"))

    try:
        # if brkword is None:
        if not direction:
            raise GoError("GO where ?")
        if direction == "rope":
            direction = "up"
        exit_id = EXITS.get(direction)
        if exit_id is None:
            raise GoError("Thats not a valid direction")

        user.go(exit_id)
    except GoError as e:
        flash(e)

    return redirect(url_for("mudexe.play_game"))


@mudexe.route("/quit")
def quit():
    """
    Quit game
    """
    user = load_user()
    if user is None:
        return redirect(url_for("mudexe.start_game", username="User"))

    try:
        user.quit()
    except GoError as e:
        flash(e)

    return redirect(url_for("mudexe.play_game"))
