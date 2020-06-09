from django.http import HttpResponse
from .api import action_api


def _get(request, key):
    if key in request.GET.keys():
        return request.GET[key]
    return ''


def index(request):
    action = _get(request, 'action')
    token = _get(request, 'token')
    uid = _get(request, 'uid')
    message = _get(request, 'message')
    json_result = ''
    if action == 'login':
        json_result = action_api.login_get_qr_code(token, uid)
    elif action == 'login_get_qrcode':
        json_result = action_api.login_get_qr_code(token, uid)
    elif action == 'login_get_state':
        json_result = action_api.login_get_state(token, uid)
    elif action == 'login_verify_get':
        json_result = action_api.login_verify_get(token, uid, message)
    elif action == 'login_verify_set':
        json_result = action_api.login_verify_set(token, uid, message)
    elif action == 'validate':
        json_result = action_api.validate_csdn(token, uid, message)
    elif action == 'validate_get_state':
        json_result = action_api.validate_get_state(token, uid, message)
    return HttpResponse(json_result)


def login(request):
    token = _get(request, 'token')
    uid = _get(request, 'uid')
    json_result = action_api.login_get_qr_code(token, uid)
    return HttpResponse(json_result)


def login_get_qrcode(request):
    token = _get(request, 'token')
    uid = _get(request, 'uid')
    json_result = action_api.login_get_qr_code(token, uid)
    return HttpResponse(json_result)


def login_get_state(request):
    token = _get(request, 'token')
    uid = _get(request, 'uid')
    json_result = action_api.login_get_state(token, uid)
    return HttpResponse(json_result)


def login_verify_get(request):
    token = _get(request, 'token')
    uid = _get(request, 'uid')
    message = _get(request, 'message')
    json_result = action_api.login_verify_get(token, uid, message)
    return HttpResponse(json_result)


def login_verify_set(request):
    token = _get(request, 'token')
    uid = _get(request, 'uid')
    message = _get(request, 'message')
    json_result = action_api.login_verify_set(token, uid, message)
    return HttpResponse(json_result)


def validate(request):
    token = _get(request, 'token')
    uid = _get(request, 'uid')
    message = _get(request, 'message')
    json_result = action_api.validate_csdn(token, uid, message)
    return HttpResponse(json_result)


def validate_get_state(request):
    token = _get(request, 'token')
    uid = _get(request, 'uid')
    message = _get(request, 'message')
    json_result = action_api.validate_get_state(token, uid, message)
    return HttpResponse(json_result)
