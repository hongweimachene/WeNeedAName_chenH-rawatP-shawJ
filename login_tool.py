from functools import wraps
from flask import session, redirect, url_for
from util.user import User


def login_required(f):
    '''Login function'''
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            session['prev_url'] = url_for(f"{f.__name__}")
            return redirect(url_for('login'))
    return wrap

def current_user():
    if 'username' in session:
        return User(User.get_by_username(session['username']))
