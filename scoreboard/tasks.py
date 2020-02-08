import celery
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from celery.signals import worker_process_init

from .models import DateResults, TeamsScores

from app import create_app
from models import db


@worker_process_init.connect
def init_celery_flask_app(**kwargs):
    app = create_app()
    app.app_context().push()


@celery.task()
def fetch_data():
    date = datetime.today().date() - timedelta(days=1)
    date_to_url = str(date).replace('-', '')
    URL = f'https://www.espn.com/nba/scoreboard/_/date/{date_to_url}'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    teams = soup.find_all("tbody", {"id": "teams"})
    if not soup and not teams:
        return
    if db.session.query(db.exists().where(DateResults.date==date)).scalar():
        return
    date_results_model = DateResults(date=date)
    date_results_model.save()
    for i in teams:
        away = i.find("tr", {"class": "away"})
        home = i.find("tr", {"class": "home"})
        data = {
            'away_name': away.find('span', {'class': 'sb-team-short'}).text,
            'away_score': int(away.find('td', {'class': 'total'}).text),
            'home_name': home.find('span', {'class': 'sb-team-short'}).text,
            'home_score': int(home.find('td', {'class': 'total'}).text),
            'date_results_id': date_results_model.id
        }
        teams_scores_model = TeamsScores(**data)
        teams_scores_model.save()

    driver.close()
    return
