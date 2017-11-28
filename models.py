# encoding:utf-8

from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash


class User(db.Model):
    # __tablename__ == 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self,*args,**kwargs):
        telephone = kwargs.get('telephone')
        username = kwargs.get('username')
        password = kwargs.get('password')

        self.telephone = telephone
        self.username = username
        self.password = generate_password_hash(password)

    def check_password(self,raw_password):
        result = check_password_hash(self.password,raw_password)
        return result

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', backref=db.backref('questions'))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))  #答案是给哪个问题写的，所以要保存问题的id
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))        #答案是由谁发布的

    question = db.relationship('Question',backref=db.backref('answers'
                               ,order_by=id.desc())  )  #答案依赖的是哪个question模型,可以看某个question的所有answer
    author = db.relationship('User',backref=db.backref('answers'))      #某个用户发布了哪些answers