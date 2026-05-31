from typing import Any, Dict
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_email(
    subject: str, to: str, context: Dict[str, Any], template_name: str
) -> None:
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER

    send_mail(
        subject,
        plain_message,
        from_email,
        [to],
        fail_silently=False,
        html_message=html_message,
    )
