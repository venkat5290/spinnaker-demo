from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '042b7f40fc36a987bd1338d0'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/static/upload/'
db.init_app(app)
with app.app_context():
    from market import routes # Import routes
    db.create_all()

