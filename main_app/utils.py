from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from main_app.tokens import account_activation_token


def send_email(request, user):
    current_site = get_current_site(request)
    email = EmailMessage(
        "Activate your GameMuster account",
        render_to_string('email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }),
        to=[user.email]
    )
    email.send()
