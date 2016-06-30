from init import db, app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(20))
    pw_hash = db.Column(db.String(64))


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(50))
    title = db.Column(db.String)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship('User', backref='questions')


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship('User', backref='answers')
    question = db.relationship('Question', backref='answers')
    thumbs_up = db.Column(db.Integer)
    thumbs_down = db.Column(db.Integer)


class Thumbs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    value = db.Column(db.Boolean)
    user = db.relationship('User', backref='ratings')
    answer = db.relationship('Answer')


class QuestionTag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    tag = db.Column(db.String(50))
    question = db.relationship('Question', backref='tags')

db.create_all(app=app)