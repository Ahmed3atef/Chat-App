from django.conf import settings
from django.urls import Resolver404, resolve


def show_toolbar(request):
    """
    Callback for django-debug-toolbar to decide visibility.
    Show only when DEBUG is on; never raise if path does not resolve.
    """
    if not settings.DEBUG:
        return False
    try:
        resolve(request.path)
    except Resolver404:
        return False
    return True