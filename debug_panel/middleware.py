"""
Debug Panel middleware
"""
from debug_toolbar.middleware import DebugToolbarMiddleware, show_toolbar
from django.core.urlresolvers import reverse, resolve, Resolver404
from django.http import HttpResponseRedirect
from django.shortcuts import render
import threading
import time

from debug_panel.cache import cache

# the urls patterns that concern only the debug_panel application
import debug_panel.urls
from debug_toolbar import settings as dt_settings
from debug_toolbar import middleware
from django.conf import settings
from debug_toolbar.toolbar import DebugToolbar
def show_toolbar(request):
        """
        Replaces the default function to determine whether to show the toolbar on a given page.
        """
        if request.META.get('REMOTE_ADDR', None) not in settings.INTERNAL_IPS:
            return False

        #Prevent ajax requests from being processed if ajax is disabled
        if request.is_ajax():
            if not DebugToolbar(request).get_panel_by_id('AjaxPanel').enabled:
                return False
        
        return bool(settings.DEBUG)

middleware.show_toolbar = show_toolbar

class DebugPanelMiddleware(DebugToolbarMiddleware):
    """
    Middleware to set up Debug Panel on incoming request and render toolbar
    on outgoing response.
    """


    def process_request(self, request):
        """
        Try to match the request with an URL from debug_panel application.

        If it matches, that means we are serving a view from debug_panel,
        and we can skip the debug_toolbar middleware.

        Otherwise we fallback to the default debug_toolbar middleware.
        """
        try:
            res = resolve(request.path, urlconf=debug_panel.urls)
        except Resolver404:

            #return super(DebugPanelMiddleware, self).process_request(request)


            if show_toolbar(request):
                return super(DebugPanelMiddleware, self).process_request(request)
            else:
                return None

        return res.func(request, *res.args, **res.kwargs)


    def process_response(self, request, response):
        """
        Since there is no hook to intercept and change rendering of the default
        debug_toolbar middleware, this is mostly a copy the original debug_toolbar
        middleware.

        Instead of rendering the debug_toolbar inside the response HTML, it's stored
        in the Django cache.

        The data stored in the cache are then reachable from an URL that is appened
        to the HTTP response header under the 'X-debug-data-url' key.
        """
        __traceback_hide__ = True
        ident = threading.current_thread().ident
        toolbar = self.__class__.debug_toolbars.get(ident)
        if not toolbar:
            return response
        if isinstance(response, HttpResponseRedirect):
            if not toolbar.config['INTERCEPT_REDIRECTS']:
                return response
            redirect_to = response.get('Location', None)
            if redirect_to:
                cookies = response.cookies
                response = render(
                    request,
                    'debug_toolbar/redirect.html',
                    {'redirect_to': redirect_to}
                )
                response.cookies = cookies

        for panel in toolbar.panels:
            panel.process_response(request, response)

        cache_key = "%f" % time.time()
        cache.set(cache_key, toolbar.render_toolbar())

        response['X-debug-data-url'] = request.build_absolute_uri(
            reverse('debug_data', urlconf=debug_panel.urls, kwargs={'cache_key': cache_key}))

        del self.__class__.debug_toolbars[ident]
        return response
