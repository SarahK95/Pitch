from unicodedata import category
from flask import render_template,redirect, url_for
from . import main
from .forms import PitchForm, CommentForm
from flask_login import login_required, current_user
from ..models import Pitches, Comment, User, Upvote, Downvote

@main.route('/')
def index():
    pitches=Pitches.query.all()
    product=Pitches.query.filter_by(category='product').all()
    pickup=Pitches.query.filter_by(category='pickup').all()
    interview=Pitches.query.filter_by(category='interview').all()
    promotion=Pitches.query.filter_by(category='promotion').all()
    
    return render_template('index.html', pitches=pitches ,product=product, pickup=pickup, interview=interview, promotion=promotion)

@main.route('/pitches')
@login_required
def pitches():
    pitches= Pitches.query.all()
    upvote = Upvote.query.all()
    user = current_user
    return render_template('pitch.html', pitches=pitches, upvote=upvote, user=user)

@main.route('/new_pitch', methods=['GET', 'POST'])
@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        title = form.title.data
        pitch = form.pitch.data
        category = form.category.data
        user_id = current_user._get_current_object().id
        new_pitch = Pitches(pitch=pitch, title=title, category=category, user_id=user_id)
        new_pitch.save()
        return redirect(url_for('main.index'))
    return render_template('pitch.html', form=form)



        
