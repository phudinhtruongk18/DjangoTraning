from datetime import datetime, timedelta
from typing import NoReturn
from .models import NomalUser

from django.core.mail import EmailMessage

from app.settings import EMAIL_HOST_USER

def report_user_daily() -> NoReturn:
    """ Daily report for admin the number of registered users """
    user_in_day = NomalUser.objects.filter(date_joined__gte=datetime.now()-timedelta(days=1))

    mail_subject = 'New user daily report'
    html_message = f"""
    <h1>New user daily report</h1>
    <p>There are {user_in_day.count()} user in the last 24h</p>
    <div>Detail:</div>
    <ul>
        {''.join([f'<li>{user.full_name()}</li>' for user in user_in_day])}
        
    """

    message = EmailMessage(mail_subject, html_message, EMAIL_HOST_USER, [EMAIL_HOST_USER])
    message.content_subtype = 'html' # this is required because there is no plain text email message
    message.send()

    # return here
