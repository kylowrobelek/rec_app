from celery_module.celery import make_celery
from flask import Flask, request, jsonify

from models import db
from scoreboard.views import scoreboard_view


def create_app():
    app = Flask(__name__)
    app.register_blueprint(scoreboard_view)

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
    return app


celery = make_celery(create_app())


if __name__ == '__main__':
    app = create_app()
    app.run()
