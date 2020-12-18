__author__ = 'Administrator'
from flask import url_for, redirect, make_response, render_template, Flask
from app_src import app\
    # , socketio
from app_src.main import main
from app_src.login import login
from app_src.run import run
# from app.dataExtract import dataExtract
from app_src.run.runFunc import lineBreak
from conf import port
# from flask_cors import CORS
# cors = CORS(app, resources={r"*": {"origins": "*"}})
import warnings
warnings.filterwarnings("ignore")

app.register_blueprint(main, url_prefix='/main')
app.register_blueprint(login, url_prefix='/login')
app.register_blueprint(run, url_prefix='/run')
# app.register_blueprint(dataExtract, url_prefix='/dataExtract')

env = app.jinja_env
env.filters['lineBreak'] = lineBreak


@app.route('/')
def hello_world():
    return redirect(url_for('login._login'))


@app.errorhandler(404)
def not_found(error):
    print(error)
    resp = make_response(render_template('about/404.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


@app.errorhandler(500)
def error_Exception(error):
    print("raise error 500!", error)
    resp = make_response(render_template('about/500.html', reason=error), 500)
    resp.headers['X-Something'] = 'A value'
    return resp


@app.errorhandler(Exception)
def error_Exception(error):
    print(error)
    resp = make_response(render_template('about/500.html'), 500)
    resp.headers['X-Something'] = 'A value'
    return resp

# 打包exe：
## pyinstaller -F mainApp.py -i docs/coverIcon.ico --add-data=app_src/templates;app_src/templates --add-data=app_src/static;app_src/static --add-data=app_src/sqliteDB;app_src/sqliteDB
## pyinstaller mainApp.spec

# ssl_keys = ('sslkey/server-cert.cer', 'sslkey/server-key.key')
if __name__ == '__main__':
    # app.run(port=port, host='0.0.0.0', debug=True,
    #         # ssl_context=ssl_keys
    #         )
    app.run(host='0.0.0.0', debug=True, port=port)
    # socketio.run(app, host='0.0.0.0', debug=True, port=port)



