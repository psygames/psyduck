from django.http import HttpResponse
from .api import action_api
import sys
import json


def _get(request, key):
    if key in request.GET.keys():
        return request.GET[key]
    return ''


def index(request):
    action = _get(request, 'action')

    if hasattr(sys.modules[__name__], action):
        return getattr(sys.modules[__name__], action)(request)

    _err = {'status': 'error', 'message': '请求的 action 不存在。'}
    json_result = json.dumps(_err, ensure_ascii=False, indent=4)
    return HttpResponse(json_result)


# login
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


# validate
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


# update
def update(request):
    token = _get(request, 'token')
    uid = _get(request, 'uid')
    message = _get(request, 'message')
    json_result = action_api.update_csdn(token, uid, message)
    return HttpResponse(json_result)


def update_get_state(request):
    token = _get(request, 'token')
    uid = _get(request, 'uid')
    message = _get(request, 'message')
    json_result = action_api.update_get_state(token, uid, message)
    return HttpResponse(json_result)


# list
def user_list(request):
    uid = _get(request, 'uid')
    json_result = action_api.user_list(uid)
    return HttpResponse(json_result)
