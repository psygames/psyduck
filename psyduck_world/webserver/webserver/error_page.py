from django.http import HttpResponse
import json


def _error_response(code, message):
    json_result = json.dumps({'status': 'error', 'message': message, 'code': code}, ensure_ascii=False, indent=4)
    return HttpResponse(json_result)


def page_400(request, exception):
    return _error_response(400, 'request error.')


def page_404(request, exception):
    return _error_response(404, 'page not found.')


def page_500(request):
    return _error_response(500, 'server internal error.')
