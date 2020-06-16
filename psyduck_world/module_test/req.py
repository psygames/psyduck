import requests
import json

action_mode = True
post_mode = True


def req(_action: str, _params: dict) -> dict:
    _address = 'http://127.0.0.1:8000/psyduck'
    if action_mode:
        _address += '/' + _action
    else:
        _params['action'] = _action
    if post_mode:
        _doc = requests.post(_address, _params)
    else:
        _param_str = ''
        _first = True
        for k in _params:
            if _first:
                _param_str += f'?{k}={_params[k]}'
            else:
                _param_str += f'&{k}={_params[k]}'
            _first = False
        _doc = requests.get(_address + _param_str)
    _json = json.loads(_doc.content)
    return _json


def req_simple(_action: str, _token: str = '', _params=None) -> dict:
    if _params is None:
        _params = {}
    _params['token'] = _token
    _params['uid'] = 'admin'
    return req(_action, _params)
