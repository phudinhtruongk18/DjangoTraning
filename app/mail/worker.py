from django.template.loader import render_to_string 
from django.core.mail import EmailMessage

from app.settings import EMAIL_HOST_USER

def mailing_healchecl(plugins):
    mail_subject = 'Heal check report'
    html_message = render_to_string('mail/mail.html', {
        "plugins":plugins
    })

    message = EmailMessage(mail_subject, html_message, EMAIL_HOST_USER, [EMAIL_HOST_USER])
    message.content_subtype = 'html' # this is required because there is no plain text email message
    message.send()