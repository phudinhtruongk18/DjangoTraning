from django.db import transaction
from django.core.mail import EmailMultiAlternatives

from core.exceptions import ApplicationError
from styleguide_example.common.services import model_update
from styleguide_example.emails.models import Email



# @transaction.atomic
def email_send(email: Email) -> Email:
    if email.status != Email.Status.SENDING:
        raise ApplicationError(f"Cannot send non-ready emails. Current status is {email.status}")

    subject = email.subject
    from_email = "styleguide-example@hacksoft.io"
    to = email.to

    html = email.html
    plain_text = email.plain_text

    msg = EmailMultiAlternatives(subject, plain_text, from_email, [to])
    msg.attach_alternative(html, "text/html")

    # msg.send()
    # select for update

    email, _ = model_update(
        instance=email,
        fields=["status", "sent_at"],
        data={
            "status": Email.Status.SENT,
            # "sent_at": timezone.now()
        }
    )
    return email