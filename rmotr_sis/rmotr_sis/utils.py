from __future__ import division, unicode_literals, absolute_import

import os

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import send_mail


def send_template_mail(subject, template, from_email, recipient_list,
                       context=None, **kwargs):
    """Extends django.core.mail.send_mail to accept HTML templates"""

    context = context or {}

    html_message = render_to_string(
        os.path.join(settings.EMAIL_TEMPLATE_LOCATION, template),
        context
    )
    text_message = strip_tags(html_message)

    send_mail(subject, text_message, from_email, recipient_list,
              html_message=html_message, **kwargs)
