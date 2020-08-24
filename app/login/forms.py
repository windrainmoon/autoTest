__author__ = 'Administrator'
from app.common.common import db
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired





class LogInForm(FlaskForm):
    """ Log in form. """
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


from flask_login import UserMixin  # 引入用户基类
from werkzeug.security import check_password_hash



class User(UserMixin):
    def __init__(self, user):
        self.id = user[0]
        self.username = user[1]
        self.password_hash = user[2]
        self.head = user[3]


    def verify_password(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)


    def get_id(self):
        return self.id

    @staticmethod
    def get(user_id):
        """根据用户ID获取用户实体，为 login_user 方法提供支持"""
        if not user_id:
            return None
        cursor = db.cursor()
        result = cursor.execute("select count(1) from user where user_id=:v1", [user_id]).fetchone()
        if result[0] != 0:
            users = cursor.execute("select user_id, user_name, user_password, user_head from user where user_id=:v1", [user_id]).fetchone()
            cursor.close()
            return User(users)
        cursor.close()
        return None



def get_user(user_id):
    """根据用户ID获取用户实体，为 login_user 方法提供支持"""
    if not user_id:
        return None
    cursor = db.cursor()

    result = cursor.execute("select count(1) from user where user_id=:v1", [user_id]).fetchone()
    if result[0] != 0:
        users = cursor.execute("select user_id, user_name, user_password, user_head from user where user_id=:v1", [user_id]).fetchone()
        cursor.close()
        return users
    cursor.close()
    return None