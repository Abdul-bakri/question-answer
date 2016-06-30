import base64
import bcrypt
import flask
import markdown
import models
import os
from sqlalchemy.orm import joinedload
from markupsafe import Markup
from init import app, db
from sqlalchemy import desc


@app.before_request
def setup_csrf():
    if 'csrf_token' not in flask.session:
        flask.session['csrf_token'] = base64.b64encode(os.urandom(32)).decode('ascii')


@app.before_request
def setup_user():
    if 'auth_user' in flask.session:
        user = models.User.query.get(flask.session['auth_user'])
        flask.g.user = user


@app.route('/')
def index():
    # initialize database if it's not made
    if os.path.exists('project3.db'):
        recent_posts = models.Question.query.order_by(desc(models.Question.id)).limit(25).all()
    else:
        question = models.Question()
        question.title = 'Initializing Database with first question!'
        question.subject = 'initial subject'
        question.creator_id = 'Anonymous Bob'
        db.session.add(question)
        db.session.commit()
        recent_posts = models.Question.query.order_by(desc(models.Question.id)).limit(25).all()
    return flask.render_template('index.html', csrf_token=flask.session['csrf_token'], recent_posts=recent_posts)


@app.route('/new_question')
def new_question():
    return flask.render_template('new_question.html')


@app.route('/add_question', methods=['POST'])
def add_question():
    question = models.Question()
    question.title = flask.request.form['question']
    question.subject = flask.request.form['subject']
    question.creator_id = flask.session['auth_user']
    db.session.add(question)
    db.session.commit()
    return flask.redirect(flask.url_for('questions', aid=question.id), code=303)


@app.route('/questions/<int:aid>')
def questions(aid):
    question = models.Question.query.get(aid)
    answers = models.Answer.query.filter_by(question_id=aid).all()
    ratings = []
    if question is None:
        flask.abort(404)
    else:
        if 'auth_user' in flask.session:
            for answer in answers:
                if models.Thumbs.query.filter_by(answer_id=answer.id, user_id=flask.session['auth_user']).first():
                    ratings.append(models.Thumbs.query.filter_by(answer_id=answer.id, user_id=flask.session['auth_user']).first())
            print(ratings)
            thumb = ratings is not None
            return flask.render_template('questions.html', question=question, answers=answers,
                                         thumb=thumb, ratings=ratings)
    return flask.render_template('questions.html', question=question, answers=answers)


@app.route('/add_answer', methods=['POST'])
def add_answer():
    answer = models.Answer()
    answer.content = flask.request.form['content']
    answer.question_id = flask.request.form['question_id']
    answer.creator_id = flask.session['auth_user']
    answer.thumbs_up = 0
    answer.thumbs_down = 0
    db.session.add(answer)
    db.session.commit()
    return flask.redirect(flask.url_for('questions', aid=answer.question_id, code=303))


@app.route('/login')
def login():
    return flask.render_template('login.html')


@app.route('/login', methods=['POST'])
def handle_login():
    login = flask.request.form['user']
    password = flask.request.form['password']
    user = models.User.query.filter_by(login=login).first()
    if user is not None:
        pw_hash = bcrypt.hashpw(password.encode('utf8'), user.pw_hash)
        if pw_hash == user.pw_hash:
            flask.session['auth_user'] = user.id
            return flask.redirect(flask.request.form['url'], 303)
    return flask.render_template('login.html', state='bad')


@app.route('/create_user', methods=['POST'])
def create_user():
    login = flask.request.form['user']
    password = flask.request.form['password']
    if password != flask.request.form['confirm']:
        return flask.render_template('login.html', state='password-mismatch')
    if len(login) > 20:
        return flask.render_template('login.html', state='bad-username')
    existing = models.User.query.filter_by(login=login).first()
    if existing is not None:
        return flask.render_template('login.html', state='username-used')
    user = models.User()
    user.login = login
    user.pw_hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(15))
    db.session.add(user)
    db.session.commit()
    flask.session['auth_user'] = user.id
    return flask.redirect(flask.url_for('show_user', name=login), 303)


@app.route('/user/<name>')
def show_user(name):
    user = models.User.query.filter_by(login=name).first()
    if user is None:
        flask.abort(404)
    return flask.render_template('user.html', user=user)


@app.route('/logout')
def logout():
    del flask.session['auth_user']
    return flask.redirect(flask.url_for('login'))


@app.errorhandler(404)
def not_found(err):
    return flask.render_template('404.html', path=flask.request.path), 404

