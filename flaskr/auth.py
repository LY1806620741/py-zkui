import functools
from flask import (
    Blueprint, flash, g, redirect,abort, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

defaultuser="jieshao"

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    elif request.method == 'GET':
        #fastlogin if no password
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (defaultuser,)
        ).fetchone()

        if user is None:
            db.execute(
               'Insert into user (username,password) values(?,?)',(defaultuser,"",)
            )
            db.commit()
            user=db.execute(
               'select id from user where username=?',(defaultuser,)
            )
            if user is not None:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for(''))
        else:
            if user['password']=="":
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('index.index'))

    return render_template('auth/login.html')

@bp.route('/info', methods=('GET', 'POST'))
def info():
    if g.user is None:
        return "",0
    else:
        return {'username':g.user['username'],'haspass':g.user['password']!=''}
    

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return ""

@bp.route('/changepass',methods=['POST'])
def changepass():
    data=request.get_json(silent=True)
    if 'checkpass' in data:
        if (check_password_hash(g.user['password'], '' if data['checkpass']==None else data['checkpass'])):
            return ''
        else:
            return '5',400
    elif 'oldpass' in data:
        if (check_password_hash(g.user['password'], '' if data['oldpass']==None else data['oldpass'])):
            db = get_db()
            db.execute(
                'update user set password=? where username=?',('' if data['newpass']=='' or data['newpass']==None else generate_password_hash(data['newpass']) ,g.user['username'])
            )
            db.commit()
            g.user=None
            return ''
        else:
            return '5',400
    elif 'newpass' in data:
        if data['newpass']==None:
            data['newpass']=''
        if g.user['password']=='':
            db = get_db()
            db.execute(
                'update user set password=? where username=?',('' if data['newpass']=='' or data['newpass']==None else generate_password_hash(data['newpass']) ,g.user['username'])
            )
            db.commit()
            g.user=None
            return ''
    return '',400

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def api_need_login(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return abort(401)

        return view(**kwargs)

    return wrapped_view