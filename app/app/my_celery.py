import os
from celery import Celery
from celery.schedules import crontab
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object('django.conf:settings', namespace='CELERY')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 100 seconds.
    sender.add_periodic_task(100.0, test.s('hello'), name='add every 10')

    # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task
def test(arg):
    print(f"Pro test{ arg}")

def add(x, y):
    z = x + y
    print(z)

if __name__ == '__main__':
    # print(app)
    app.start()
