from django.conf import settings


if not hasattr(settings, 'UNDER_CONSTRUCTION'):
    settings.UNDER_CONSTRUCTION = False
