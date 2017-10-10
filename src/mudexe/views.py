from flask import Blueprint, render_template
# from flask import Blueprint, render_template, redirect, url_for, flash

# from app import db

# from .models import GameSession
# from .forms import GameSessionForm


mudexe = Blueprint('mudexe', __name__)


@mudexe.route("/start/<username>")
def start_game(username):
    """
    Render start page
    """
    # campaigns = Campaign.query.filter(Campaign.gs_id==rpg.id).all()
    # sessions = GameSession.query.filter_by(campaign_id=campaign_id).order_by(GameSession.real_date.desc()).paginate(page, app.config.get('RECORDS_ON_PAGE'))
    return render_template(
        'mudexe/view.html',
        title="Sessions",
        # campaign=campaign,
        # campaign_id=campaign_id,
        # items=sessions.items,
        # pagination=sessions,
    )
