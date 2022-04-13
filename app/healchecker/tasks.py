from __future__ import absolute_import, unicode_literals

from celery import shared_task

from user.models import NomalUser

from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.db.models.signals import (
        post_save,
)

from django.contrib.auth.tokens import default_token_generator
from app.settings import EMAIL_HOST_USER
from celery import shared_task
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

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

@receiver(post_save, sender=NomalUser)
def user_post_save_receiver(sender, instance, created, *args, **kwargs):
    """
    after saved in the database
    """
    uid = urlsafe_base64_encode(force_bytes(instance.pk))
    current_site = Site.objects.get_current()
    print("current_site", current_site)
    token = default_token_generator.make_token(instance)
    email = instance.email
    send_mai_to_kid.delay(created,str(current_site), email,str(current_site.domain),uid,token)