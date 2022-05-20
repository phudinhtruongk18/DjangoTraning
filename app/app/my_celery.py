import os
from celery import Celery
from celery.schedules import crontab
# from celery.tasks import periodic_task


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
    from healchecker.healcheck import heal_check_pro
    from mail.worker import report_user_daily

    @app.task
    def daily_task():
        report_user_daily()

    @app.task
    def heal_check_every_minute():
        heal_check_pro()

    # Calls healcheck every minutes
    sender.add_periodic_task(
        60.0, 
        heal_check_every_minute.s(), 
        name='heal check every minute')

    # Executes every morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30),
        daily_task.s(),
        name='Daily task',
    )

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# @app.task
# def add(x, y):
#     z = x + y
#     print(z)

from celery import shared_task
from django.core.mail import EmailMessage
from app.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string 

@shared_task(name="Mail new kid",autoretry_for=(Exception,), retry_backoff=2)
def send_mai_to_kid(created,current_site,email,domain,uid,token):
    # autoretry_for=(Exception,), retry_backoff=2
    if created:
        print("Send email to", email)
        mail_subject = 'Activate your Aram Account'
        text_message = render_to_string('user/active_email.html', {
            'user': email,
            'current_site' : current_site,
            'domain': domain,
            'uid': uid,
            'token': token,
        })

        message = EmailMessage(mail_subject, text_message, EMAIL_HOST_USER, [email])
        message.send()
    else:
        print(email, "was just saved")

if __name__ == '__main__':
    # print(app)
    app.start()
