import unittest
from datetime import datetime, timedelta

from app import create_app, db
from scoreboard.models import DateResults, TeamsScores


class ScoreboardTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.date = datetime.today().date() - timedelta(days=1)
        with self.app.app_context():
            db.create_all()
            date_result_model = DateResults(
                date=self.date)
            date_result_model.save()
            teams_scores = {
                'away_name': 'some away name',
                'away_score': 12,
                'home_name': 'some home name',
                'home_score': 13,
                'date_results_id': date_result_model.id
            }
            teams_scores_model = TeamsScores(**teams_scores)
            teams_scores_model.save()

    def test_dates(self):
        response = self.client().get('/dates')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_score_actual(self):
        response = self.client().get('/score/actual')
        self.assertEqual(response.status_code, 200)
        self.assertIn('some away name', str(response.json))

    def test_score_date(self):
        response = self.client().get('/score/date', query_string={
            'date': self.date.strftime('%Y-%m-%d')})
        self.assertEqual(response.status_code, 200)
        self.assertIn('some away name', str(response.json))

    def test_score_date_no_value(self):
        response = self.client().get('/score/date')
        self.assertEqual(response.status_code, 200)
        self.assertIn('no date provided', str(response.data))

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()

