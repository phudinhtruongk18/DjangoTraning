from __future__ import absolute_import, unicode_literals

from celery import shared_task

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from app.settings import EMAIL_HOST_USER

@shared_task(name="add")
def add(a,b):
    print("Email task will be similar")
    return a+b

@shared_task(name="Mail new kid")
def send_mai_to_kid(created,current_site,email,domain,uid,token):
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
