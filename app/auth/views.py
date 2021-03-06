from flask import render_template,url_for,redirect, flash, request
from . import auth
from ..models import User
from .forms import SignUpForm, LoginForm
from .. import db
from ..email import email_message
from flask_login import login_user, logout_user, login_required



@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        # email_message('Welcome to pitch', 'email/welcome_user', user.email, user=user)
        return redirect(url_for('auth.login'))
    
    title = "Create account"
    return render_template('auth/signup.html', signup_form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username = login_form.username.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(url_for('main.new_pitch'))
        flash('Invalid username or Password')

    title = "User login"
    return render_template('auth/login.html',login_form = login_form,title=title)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


