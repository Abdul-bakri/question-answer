# import time
import flask
from init import app, db
import models


@app.route('/api/update-thumbs-up', methods=['POST'])
def update_thumbs_up():
    print('in update_thumbs_up')
    if 'auth_user' not in flask.session:
        flask.abort(403)
    user_id = flask.session['auth_user']
    print('user id:', user_id)
    if flask.request.form['_csrf_token'] != flask.session['csrf_token']:
        flask.abort(400)
    answer_id = flask.request.form['answer_id']
    print('answer id:', answer_id)
    want_thumbs_up = flask.request.form['want_thumbs_up'] == 'true'
    print('want_thumbs_up:', want_thumbs_up)
    thumb_up = models.Thumbs.query.filter_by(answer_id=answer_id, user_id=user_id).first()
    print('after thumb model call')

    answer = models.Answer.query.filter_by(id=answer_id).first()

    if want_thumbs_up:
        if thumb_up is None:
            thumb_up = models.Thumbs()
            thumb_up.user_id = user_id
            thumb_up.answer_id = answer_id
            thumb_up.value = 1
            db.session.add(thumb_up)
            db.session.commit()

            if answer.thumbs_up is None:
                answer.thumbs_up = 1
            else:
                answer.thumbs_up += 1
            db.session.add(answer)
            db.session.commit()
            return flask.jsonify({'result': 'ok'})
        else:
            app.logger.warn('answer %s already rated by %s', answer_id, user_id)
            return flask.jsonify({'result': 'already-rated'})
    else:
        if thumb_up is not None:
            db.session.delete(thumb_up)
            db.session.commit()

            answer.thumbs_up -= 1
            db.session.add(answer)
            db.session.commit()
            return flask.jsonify({'result': 'ok'})
        else:
            return flask.jsonify({'result': 'not-rated'})


@app.route('/api/update-thumbs-down', methods=['POST'])
def update_thumbs_down():
    print('in update_thumbs_down')
    if 'auth_user' not in flask.session:
        flask.abort(403)
    user_id = flask.session['auth_user']
    print('user id:', user_id)
    if flask.request.form['_csrf_token'] != flask.session['csrf_token']:
        flask.abort(400)
    print('after if')
    answer_id = flask.request.form['answer_id']
    print('answer id:', answer_id)
    want_thumbs_down = flask.request.form['want_thumbs_down'] == 'true'
    print('want_thumbs_down:', want_thumbs_down)
    thumb_down = models.Thumbs.query.filter_by(answer_id=answer_id, user_id=user_id).first()
    print('after thumb model call')

    answer = models.Answer.query.filter_by(id=answer_id).first()

    if want_thumbs_down:
        if thumb_down is None:
            thumb_down = models.Thumbs()
            thumb_down.user_id = user_id
            thumb_down.answer_id = answer_id
            thumb_down.value = 0
            db.session.add(thumb_down)
            db.session.commit()

            if answer.thumbs_up is None:
                answer.thumbs_up = -1
            else:
                answer.thumbs_up -= 1
            db.session.add(answer)
            db.session.commit()
            return flask.jsonify({'result': 'ok'})
        else:
            app.logger.warn('answer already rated', answer_id, user_id)
            return flask.jsonify({'result': 'already-rated'})
    else:
        if thumb_down is not None:
            db.session.delete(thumb_down)
            db.session.commit()

            answer.thumbs_up += 1
            db.session.add(answer)
            db.session.commit()
            return flask.jsonify({'result': 'ok'})
        else:
            return flask.jsonify({'result': 'not-rated'})