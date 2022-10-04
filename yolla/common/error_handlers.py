from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _


def status_code_403(request, *args, **kwargs):
    response = render(request, 'common/error_handlers.html', {
        'label': _('Forbidden'),
        'content': '403 Forbidden',
    })
    response.status_code = 403
    return response


def status_code_404(request, *args, **kwargs):
    response = render(request, 'common/error_handlers.html', {
        'label': _('Page not found'),
        'content': '404 Not Found',
    })
    response.status_code = 404
    return response
