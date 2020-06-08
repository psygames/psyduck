from django.http import HttpResponse
from .api import action_api


def _get(request, key):
    if key in request.GET.keys():
        return request.GET[key]
    return ''


def index(request):
    token = _get(request, 'token')
    action = _get(request, 'action')
    uid = _get(request, 'uid')
    message = _get(request, 'message')
    json_result = ''
    if action == 'validate':
        json_result = action_api.validate_csdn(token, uid, message)
    elif action == 'validate_get_state':
        json_result = action_api.validate_get_state(token, uid, message)
    elif action == 'login':
        json_result = action_api.login_get_qr_code(token, uid)
    elif action == 'login_get_qrcode':
        json_result = action_api.login_get_qr_code(token, uid)
    elif action == 'login_get_state':
        json_result = action_api.login_get_state(token, uid)
    elif action == 'login_verify_get':
        json_result = action_api.login_verify_get(token, uid, message)
    elif action == 'login_verify_set':
        json_result = action_api.login_verify_set(token, uid, message)
    return HttpResponse(json_result)
