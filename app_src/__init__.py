__author__ = 'Administrator'
from flask import Flask
from flask_login import LoginManager

#-------------------------------
# from flask_socketio import SocketIO

# from flask.ext.babelex import Babel
#-------------------------------

# app = Flask(__name__)
# # socketio = SocketIO(app)
# app.runConfig['DEBUG'] = True
# # babel = Babel(app)
# app.runConfig['SECRET_KEY'] = 'app.runConfig'
#
#


app = Flask(__name__, template_folder='templates')
# socketio = SocketIO(app)
app.config['DEBUG'] = True
# babel = Babel(app)
app.config['SECRET_KEY'] = 'app.runConfig'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'