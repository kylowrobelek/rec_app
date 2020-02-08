from datetime import datetime, timedelta
from flask import abort, Blueprint, jsonify, request, Response

from .models import DateResults, TeamsScores


scoreboard_view = Blueprint('scoreboard_view', __name__)


@scoreboard_view.route('/dates', methods=('get',))
def get_dates():
    dates = DateResults.query.all()
    return jsonify([{'id': model.id, 'date': model.date} for model in dates]), 200


@scoreboard_view.route('/score/actual', methods=('get',))
def get_scores_today():
    date = DateResults.query.filter_by(
        date=datetime.today().date() - timedelta(days=1)).first()
    scores = TeamsScores.query.filter_by(date_results_id=date.id).all()
    from pudb import set_trace; set_trace()
    data = {
        str(date.date): [{
            score.home_name: score.home_score,
            score.away_name: score.away_score
        } for score in scores]
    }
    return jsonify(data), 200


@scoreboard_view.route('/score/date', methods=('get',))
def get_scores():
    date = request.args.get('date')
    if not date:
        abort(Response('no date provided'))
    date = DateResults.query.filter_by(date=date).first()
    scores = TeamsScores.query.filter_by(date_results_id=date.id)
    data = {
        str(date.date): [{
            score.home_name: score.home_score,
            score.away_name: score.away_score
        } for score in scores]
    }
    return jsonify(data), 200
