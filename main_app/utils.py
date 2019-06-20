from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import QuerySet
from django.template.loader import render_to_string
from django.urls.converters import StringConverter
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from main_app.models import UserModel
from main_app.tokens import account_activation_token


def send_email(request, user, api=False):
    current_site = get_current_site(request)
    args_to_email = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    }
    if api:
        args_to_email['api'] = True
    email = EmailMessage(
        "Activate your GameMuster account",
        render_to_string('email.html', args_to_email),
        to=[user.email]
    )
    email.send()


class TokenConverter(StringConverter):
    regex = '[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}'


def search_in_queryset(queryset, search: str, search_field: str = 'name'):
    if queryset and search != '':
        if isinstance(queryset, QuerySet) and hasattr(queryset[0], search_field):
            query = {f"{search_field}__search": search}
            return queryset.filter(**query)
        raise AttributeError(f"queryset doesn't have {search_field} attribute")
    return queryset


def auth_token_check(uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        return user
    return None
