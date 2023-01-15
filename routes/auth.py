from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, EqualTo
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, request, Blueprint, url_for
from flask_login import LoginManager, login_user, current_user, logout_user
from app.db import db, Users

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.unauthorized_handler  # login page
def unauthorized():
    return redirect(url_for('auth.login'))


class Register_Form(FlaskForm):
    username = StringField('Name', validators=[InputRequired(), Length(min=4, max=15)])
    email = EmailField('Email', validators=[InputRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    confirm = PasswordField('Confirm Password',
                            validators=[InputRequired(), EqualTo('password', message='Passwords must match')])


class Login_Form(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])



@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).filter(Users.id == user_id).first()




@auth_blueprint.route('/auth/register', methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("misc.home"))
    form = Register_Form()
    if form.validate_on_submit():
        user = db.session.query(Users).filter(Users.email == form.email.data).first()
        if user is not None:
            form.email.errors.append('You already have an account. Please log in.')
            return render_template('register.html', form=form)

        age = request.form.get("age")
        gender = request.form.get("gender")

        print(age,gender) #not printing

        new_user = Users(name=form.username.data, email=form.email.data,
                            password=generate_password_hash(form.password.data),
                             age=age, gender=gender)

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("misc.home"))

    return render_template('register.html', form=form)


@auth_blueprint.route('/auth/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("misc.home"))

    form = Login_Form()
    if form.validate_on_submit():
        print(form.email.data)
        user = db.session.query(Users).filter(Users.email == form.email.data).first()  # None
        if user is None:
            form.email.errors.append('You do not have a account please register')

            return render_template('login.html', form=form)
        elif check_password_hash(user.password,
                                 form.password.data):  # not check_password_hash(user.password, form.password.data)

            form.password.errors.append('Please check your login details.')
            return render_template('login.html', form=form)
        else:

            login_user(user)

            return redirect(url_for("misc.home"))

    else:
        return render_template('login.html', form=form)


@auth_blueprint.route('/logout', methods=["POST", "GET"])
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
