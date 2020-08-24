__author__ = 'Administrator'
from flask import url_for, redirect

from app import app
from app.main import main
from app.login import login
from app.run import run
from app.run.runFunc import lineBreak
from conf import port


app.register_blueprint(main, url_prefix='/main')
app.register_blueprint(login, url_prefix='/login')
app.register_blueprint(run, url_prefix='/run')

env = app.jinja_env
env.filters['lineBreak'] = lineBreak


@app.route('/')
def hello_world():
    return redirect(url_for('login._login'))





if __name__ == '__main__':
    app.run(port=port, host='0.0.0.0', debug=True)







