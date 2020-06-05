from django.http import HttpResponse
from .api import action_api


def _get(request, key):
    if key in request.GET.keys():
        return request.GET[key]
    return ''


def index(request):
    _id = _get(request, 'id')
    action = _get(request, 'action')
    uid = _get(request, 'uid')
    csdn = _get(request, 'csdn')
    json_result = ''
    if action == 'validate':
        json_result = action_api.validate_csdn(_id, uid, csdn)
    return HttpResponse(json_result)
