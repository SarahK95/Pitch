from flask import render_template,redirect, url_for
from . import main
from .forms import PitchForm, CommentForm


@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    return render_template('index.html')


# @main.route('/new_pitch', methods=['GET','POST'])
# def pitch_form():
#     form = PitchForm()
#     if form.validate_on_submit():
#         title = form.title.data
#         pitch = form.pitch.data
#         category = form.category.data
#         user_id = current_user._get_current_object().id
#         new_pitch = Pitches(pitch=pitch,title=title, category=category)
#         new_pitch.save_pitch()
#         return redirect(url_for('main.index'))
#     return render_template('pitch.html', form=form)
        
