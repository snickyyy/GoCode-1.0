from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.template.loader import render_to_string


class SendingEmail:
    def create_message(self, request, template_name, user, token, **kwargs):
        context = {
            "user": user,
            "domain": get_current_site(request),
            "token": token,
            "pk": user.id,
            **(kwargs or {}),
        }
        return render_to_string(template_name, context)

    def send_email(self, subject, message, to, cc=None, **kwargs):
        email = EmailMessage(subject=subject, body=message, cc=cc, to=to, **kwargs)
        email.content_subtype = "html"
        email.send(fail_silently=settings.EMAIL_FAIL_SILENTLY)
        return email
