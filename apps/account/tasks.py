
from __future__ import absolute_import, unicode_literals
from celery import shared_task


from django.core.mail import send_mail

from OrangeMall import settings


@shared_task
def send_active_mail(subject='', content=None, to=None):
    send_mail(subject, message='',from_email=settings.EMAIL_HOST_USER, recipient_list=to, html_message=content)