# encoding:utf-8
from flask import Flask, render_template, request, redirect, url_for, session,g
import config
from exts import db
from models import User, Question,Answer
from decorator import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        if user and user.check_password(password):
            session['user_id'] = user.id  # 登录成功
            # return render_template('index.html') 错误！
            return redirect(url_for('index'))
        else:
            return u'手机号码或密码错误，请重新登录'


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该手机号码已经被注册'
        else:
            if password1 != password2:
                return u'两次密码不一致，请核对后再填写'
            else:
                user = User(telephone=telephone, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


@app.context_processor
def my_context_processor():
    if hasattr(g,'user'):
            return {'user': g.user}
    return {}


@app.route('/logout/')
def logout():
    session.pop('user_id')
    # del session['user_id']
    return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        question.author = g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>/')
def detail(question_id):
    question = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html',question=question)

@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer')
    question_id = request.form.get('question_id')
    answer = Answer(content=content)
    answer.author = g.user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))  #将question_id传到模板中？

@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user  #?

#before_request -> view func -> context_proceessor

if __name__ == '__main__':
    app.run()
