from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/users/register', methods=['POST'])
def register():
    if not User.validate(request.form):
        return redirect('/login')

    pwd = bcrypt.generate_password_hash(request.form['register_password'])

    register_form = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['register_email'],
        'password': pwd
    }

    id = User.save(register_form)
    session['user_id'] = id

    return redirect('/search')


@app.route('/users/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    # Login Failure
    if not user:
        flash('Email not registered', 'login')
        return redirect('/login')
    if not bcrypt.check_password_hash(user.password, request.form['login_password']):
        flash('Wrong password', 'login')
        return redirect('/login')

    session['user_id'] = user.id

    return redirect('/search')
