from django.http import HttpResponse
import json


def json_dict_http_response(**kwargs):
    return HttpResponse(json.dumps(dict(kwargs)))


def success_response(**kwargs):
    return json_dict_http_response(success=True, **kwargs)


def exception_response(error_msg):
    return json_dict_http_response(success=False, error_msg=error_msg)


def json_object_http_response(res):
    ret = json.dumps(res, default=lambda obj: obj.__dict__)
    return HttpResponse(ret)
