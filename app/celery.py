from celery import Celery

from app import app


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    # celery.conf.task_always_eager = True
    celery.conf.accept_content = ['pickle', 'application/json']
    celery.conf.task_serializer = 'pickle'
    # celery.conf.result_serializer = 'pickle'

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery