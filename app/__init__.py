__author__ = 'Administrator'
from flask import Flask
from flask_login import LoginManager

# from flask.ext.babelex import Babel

app = Flask(__name__)
app.config['DEBUG'] = True
# babel = Babel(app)
app.config['SECRET_KEY'] = 'app.config'




login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'