from celery import Celery

def make_celery(app):
    app = app
    celery = Celery(
        app.import_name,
        backend="http://localhost:5000",
        broker="http://localhost:5000"
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
