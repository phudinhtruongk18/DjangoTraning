import os
from celery import Celery
from celery.schedules import crontab
# from celery.tasks import periodic_task
from celery import shared_task
from django.core.mail import EmailMessage
from app.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string



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
    from mail.models import Email

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

# @shared_task(name="Mail new kid",autoretry_for=(Exception,), retry_backoff=2)
# def send_mai_to_kid(current_site,email,domain,uid,token):
#     # autoretry_for=(Exception,), retry_backoff=2
#     print("Send email to", email)
#     mail_subject = 'Activate your Aram Account'
#     text_message = render_to_string('user/active_email.html', {
#         'user': email,
#         'current_site' : current_site,
#         'domain': domain,
#         'uid': uid,
#         'token': token,
#      })
#     message = EmailMessage(mail_subject, text_message, EMAIL_HOST_USER, [email])
#     message.send()

# Lets expand the email_send task example from above, by adding error handling:
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

def _email_send_failure(self, exc, task_id, args, kwargs, einfo):
    email_id = args[0]
    email = Email.objects.get(id=email_id)

    from mail.services import email_failed

    email_failed(email)


@shared_task(name="Mail new kid",autoretry_for=(Exception,), retry_backoff=2)
def email_send(self,email_id):
    email = Email.objects.get(id=email_id)

    from mail.services import email_send

    try:
        email_send(email)
    except Exception as exc:
        # https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying
        logger.warning(f"Exception occurred while sending email: {exc}")
        self.retry(exc=exc, countdown=5)


if __name__ == '__main__':
    # print(app)
    app.start()
