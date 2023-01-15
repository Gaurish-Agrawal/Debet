from flask import Flask, render_template, redirect, request, Blueprint, session, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_uploads import UploadSet, IMAGES, configure_uploads

misc_blueprint = Blueprint('misc', __name__, template_folder='templates')


@misc_blueprint.route('/', methods=["GET", "POST"])
def index():
    return redirect(url_for("misc.home"))

@misc_blueprint.route('/home', methods=["GET", "POST"])
def home():
    return render_template("home.html")
