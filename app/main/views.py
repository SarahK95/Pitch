from unicodedata import category
from flask import render_template,redirect, url_for
from . import main
from .forms import PitchForm, CommentForm, EditProfile
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

@main.route('/comment/<int:pitch_id>', methods=['GET', 'POST'])
@login_required
def comment(pitch_id):
    form = CommentForm()
    pitch = Pitches.query.get(pitch_id)
    user = User.query.all()
    comments = Comment.query.filter_by(pitch_id=pitch_id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        pitch_id = pitch_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(
            comment=comment,
            pitch_id=pitch_id,
            user_id=user_id
        )
        new_comment.save()
        new_comments = [new_comment]
        print(new_comments)
        return redirect(url_for('.comment', pitch_id=pitch_id))
    return render_template('comment.html', form=form, pitch=pitch, comments=comments, user=user)

main.route('/user')
@login_required
def user():
    username = current_user.username
    user = User.query.filter_by(username=username).first()
    if user is None:
        return ('not found')
    return render_template('profile.html', user=user)
        
@main.route('/user/<name>/edit_profile', methods=['GET', 'POST'])
@login_required
def editprofile(name):
    form = EditProfile()
    user = User.query.filter_by(username=name).first()
    if user is None:
        error = 'The user does not exist'
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save()
        return redirect(url_for('.profile', name=name))
    return render_template('profile/update_profile.html', form=form)

@main.route('/upvote/<int:id>', methods=['GET', 'POST'])
@login_required
def upvote(id):
    pitch = Pitches.query.get(id)
    new_vote = Upvote(pitch=pitch, upvote=1)
    new_vote.save()
    return redirect(url_for('main.pitches'))


@main.route('/downvote/<int:id>', methods=['GET', 'POST'])
@login_required
def downvote(id):
    pitch = Pitches.query.get(id)
    new_down = Downvote(pitch=pitch, downvote=1)
    new_down.save()
    return redirect(url_for('main.pitches'))