from datetime import datetime, timedelta
from typing import NoReturn
from .models import NomalUser

from django.template.loader import render_to_string 
from django.core.mail import EmailMessage

from app.settings import EMAIL_HOST_USER

def report_user_daily() -> NoReturn:
    """ Daily report for admin the number of registered users """
    user_in_day = NomalUser.objects.filter(last_login__gte=datetime.now()-timedelta(days=1)).count()

    mail_subject = 'New user daily report'
    html_message = f"""
    <h1>New user daily report</h1>
    <p>There are {user_in_day} user in the last 24h</p>
    """

    message = EmailMessage(mail_subject, html_message, EMAIL_HOST_USER, [EMAIL_HOST_USER])
    message.content_subtype = 'html' # this is required because there is no plain text email message
    message.send()

    # return here
