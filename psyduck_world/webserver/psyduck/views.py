from django.http import HttpResponse
from .api import action_api
import json
from django.shortcuts import render


def _get(request, key, default=''):
    if request.method == 'POST':
        if key in request.POST:
            return request.POST.get(key)
        return default
    if key in request.GET:
        return request.GET.get(key)
    return default


def index(request):
    return render(request, 'index.html')


# login
def login(request):
    token = _get(request, 'token')
    uid = _get(request, 'uid')
    json_result = action_api.login(token, uid)
    return HttpResponse(json_result)


def login_get_state(request):
    token = _get(request, 'token')
    uid = _get(request, 'uid')
    json_result = action_api.login_get_state(token, uid)
    return HttpResponse(json_result)


def login_verify_get(request):
    token = _get(request, 'token')
    uid = _get(request, 'uid')
    phone = _get(request, 'phone')
    json_result = action_api.login_verify_get(token, uid, phone)
    return HttpResponse(json_result)


def login_verify_set(request):
    token = _get(request, 'token')
    uid = _get(request, 'uid')
    code = _get(request, 'code')
    json_result = action_api.login_verify_set(token, uid, code)
    return HttpResponse(json_result)


# update
def update(request):
    token = _get(request, 'token')
    uid = _get(request, 'uid')
    csdn = _get(request, 'csdn')
    json_result = action_api.update(token, uid, csdn)
    return HttpResponse(json_result)


def update_get_state(request):
    token = _get(request, 'token')
    uid = _get(request, 'uid')
    json_result = action_api.update_get_state(token, uid)
    return HttpResponse(json_result)


# list
def user_list(request):
    uid = _get(request, 'uid')
    json_result = action_api.user_list(uid)
    return HttpResponse(json_result)


# download
def download(request):
    token = _get(request, 'token')
    uid = _get(request, 'uid')
    csdn = _get(request, 'csdn')
    url = _get(request, 'url')
    json_result = action_api.download(token, uid, csdn, url)
    return HttpResponse(json_result)


def download_get_state(request):
    token = _get(request, 'token')
    uid = _get(request, 'uid')
    json_result = action_api.download_get_state(token, uid)
    return HttpResponse(json_result)


def download_get(request):
    _id = _get(request, 'id')
    json_result = action_api.download_get(_id)
    log("API-GET", _id)
    return HttpResponse(json_result)


def download_list(request):
    uid = _get(request, 'uid')
    csdn = _get(request, 'csdn')
    _index = int(_get(request, 'index', '0'))
    json_result = action_api.download_list(uid, csdn, _index)
    return HttpResponse(json_result)


def download_find(request):
    keyword = _get(request, 'keyword')
    _index = int(_get(request, 'index', '0'))
    json_result = action_api.download_find(keyword, _index)
    log("API-FIND", keyword)
    return HttpResponse(json_result)


def recover_action(request):
    uid = _get(request, 'uid')
    json_result = action_api.recover_action(uid)
    return HttpResponse(json_result)


# SEARCH


def _response(result_json=''):
    return HttpResponse(
        json.dumps({'result_json': result_json}),
        content_type='application/json')


def search(request):
    if request.method == 'GET':
        return HttpResponse()

    uuid = _get(request, 'murmur', '')
    keyword = _get(request, 'keyword', '')
    page = int(_get(request, 'page', '0'))
    cip = _get(request, 'cip', '')
    cname = _get(request, 'cname', '')

    if uuid == '':
        return _response('none')
    log(uuid, f'[{cname}]({cip}) [{keyword}]({page})')
    result_json = action_api.download_find(keyword, page * 10)
    return _response(result_json)


def log(uuid, msg):
    import datetime
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
    print('[{}]：{} at ({})'.format(uuid[0:6], msg, now_time))
