from django.http import HttpResponse
from .api import action_api


def _get(request, key):
    if key in request.GET.keys():
        return request.GET[key]
    return ''


def index(request):
    action = _get(request, 'action')
    uid = _get(request, 'uid')
    csdn = _get(request, 'csdn')
    if action == 'validate':
        action_api.validate_csdn(uid, csdn)
    return HttpResponse("Hello, world. You're at the polls index.")
