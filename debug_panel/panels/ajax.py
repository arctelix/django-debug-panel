from __future__ import absolute_import, unicode_literals

from django.core.handlers.wsgi import STATUS_CODE_TEXT
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _, ungettext

from debug_toolbar.panels import DebugPanel


class AjaxPanel(DebugPanel):
    """
    Panel to toggle processing ajax requests
    """
    title = _("Intercept Ajax")
    template = 'panels/ajax.html'
    ajax_requests = []
    has_content = True
    
    
    @property
    def enabled(self):
        default = 'on' if self.toolbar.config['INTERCEPT_AJAX'] else 'off'
        return self.toolbar.request.COOKIES.get('djdt' + self.panel_id, default) == 'on'

    
    def nav_subtitle(self):
        num_ajax_requests = len(self.ajax_requests)
        return ungettext("Recieved %(num_ajax_requests)d request",
                             "Recieved %(num_ajax_requests)d requests",
                             num_ajax_requests) % {'num_ajax_requests': num_ajax_requests}

    def process_request(self, request):
        if request.is_ajax() and '__debug__' not in request.path:
            self.ajax_requests.append({'path':request.path,'perams':request.REQUEST})
            self.record_stats({
                'ajax_requests': self.ajax_requests,
            })
            pass

    def process_response(self, request, response):
        pass