from debug_toolbar import settings as dt_settings
from django.conf import settings

USER_CONFIG = getattr(settings, 'DEBUG_TOOLBAR_CONFIG', {})
if 'INTERCEPT_AJAX' in USER_CONFIG:
    dt_settings.CONFIG['INTERCEPT_AJAX'] = USER_CONFIG['INTERCEPT_AJAX']
else:
    dt_settings.CONFIG['INTERCEPT_AJAX'] = True

INCLUDE_AJAX_PANEL = getattr(settings, 'INCLUDE_AJAX_PANEL', True)
if INCLUDE_AJAX_PANEL:
    dt_settings.PANELS.append('debug_panel.panels.ajax.AjaxPanel')