from django.conf import settings
# from .defaults import DEFAULT_RM_URL # Good practice for future default settings

# def get_setting(name, default):
#     return getattr(settings, name, default)

RM_URL = getattr(settings, 'RM_URL', settings.STATIC_URL)
