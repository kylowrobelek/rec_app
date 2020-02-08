from models import *


class DateResults(BaseModel):

    __tablename__ = 'date_results'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    scores = db.relationship('TeamsScores', backref='date_results', lazy=True)

    def __init__(self, *args, date):
        super().__init__(*args)
        self.date = date


class TeamsScores(BaseModel):
    __tablename__ = 'teams_scores'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    home_name = db.Column(db.String(255))
    home_score = db.Column(db.Integer)
    away_name = db.Column(db.String(255))
    away_score = db.Column(db.Integer)
    date_results_id = db.Column(db.Integer, db.ForeignKey('date_results.id'),
                                nullable=False)

    def __init__(self, *args, home_name, home_score, away_name, away_score,
                 date_results_id):
        super().__init__(*args)
        self.home_name = home_name
        self.home_score = home_score
        self.away_name = away_name
        self.away_score = away_score
        self.date_results_id = date_results_id
