from flask import Flask, request, jsonify
from models import db
import json

app = Flask(__name__)

POSTGRES = {
    'user': 'krzysiek',
    'db': 'rec_task_db',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

db.init_app(app)


@app.route('/')
def welcome_main_page():
    return jsonify('Welcome')


if __name__ == '__main__':
    app.run()
