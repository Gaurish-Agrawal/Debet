from flask import Flask
import os
from flask_bootstrap import Bootstrap5
from flask_uploads import configure_uploads
from routes.auth import auth_blueprint
from routes.auth import login_manager
from routes.misc import misc_blueprint
from routes.services import services_blueprint, images, current_user
from flask_socketio import SocketIO, send, emit, join_room
from app.db import db

# Defining secret key, app, and templates directory
template_dir = os.path.abspath('views/templates')
static_dir = os.path.abspath('views/static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


boostrap = Bootstrap5()

app.config['SECRET_KEY'] = 'zjxcghkzjxhczxcjkzhc    '
app.config['UPLOAD_FOLDER'] = "./"
app.config['UPLOADED_PHOTOS_DEST'] = "./views/static/images/debates/"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#Registering Blueprints
app.register_blueprint(auth_blueprint, url_prefix="")
app.register_blueprint(misc_blueprint, url_prefix="")
app.register_blueprint(services_blueprint, url_prefix="")


with app.app_context():
    configure_uploads(app, images)
    
    db.init_app(app)
    db.create_all()
    login_manager.init_app(app)
    boostrap.init_app(app)
    
app.run(debug=True)


