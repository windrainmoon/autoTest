__author__ = 'Administrator'
from flask_login import (current_user,
                         login_user,
                         logout_user)
from . import login
from .forms import LogInForm, User, get_user
from flask import (flash,
                   g,
                   redirect,
                   render_template,
                   request,
                   session,
                   url_for)
from app import login_manager, app
from datetime import timedelta
from app.common.common import SESSION_EXPIRE_TIME


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


# login page
@login.route('login', methods=['GET', 'POST'])
def _login():
    # if the user is already logged in redirect to homepage.
    form = LogInForm()
    print(session)
    if 'user_name' in session:
        print(session)
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=SESSION_EXPIRE_TIME)
        return redirect(url_for('main.index'))

    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        user_info = get_user(user_name)
        if user_info is None:
            flash("用户名或密码密码有误", category='error')
        else:
            user = User(user_info)  # 创建用户实体
            if user.verify_password(password):  # 校验密码  from werkzeug.security import generate_password_hash
                # flash('你已经成功的登陆', category='success')
                login_user(user, remember=remember_me)
                session.permanent = True
                app.permanent_session_lifetime = timedelta(minutes=SESSION_EXPIRE_TIME)
                session['user_name'] = user_name
                session['user_head'] = user_info[3]
                return redirect(url_for('main.index'))
            else:
                flash("用户名或密码密码有误", category='error')
    return render_template('login/login.html', title='Log In', form=form)


@login.route('/logout', methods=['GET', 'POST'])
def _logout():
    logout_user()
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('csrf_token', None)
    session.pop('_id', None)
    return redirect(url_for('login._login'))