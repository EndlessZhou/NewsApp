from django.http import HttpResponse, FileResponse, JsonResponse
import json
from user.models import *
import traceback
import filetype
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
import util
from dynamic.models import *
import urllib.parse

FILE_NOT_EXIST = "不存在头像文件"
FILE_FORMAT_ERROR = "图片文件格式错误"
PHOTO_HOST = "120.77.149.49:8000/news/dynamic/photo/"
AVATAR_HOST = "120.77.149.49:8000/news/user/get_avatar/"


# def verify(func):
#     def wrapper(request):
#         request.POST['phone_number']
#         return func(request)
#
#     return wrapper


def send(request):
    phone_number = request.POST['phone_number']
    photo = request.FILES.get('photo')
    text = request.POST['text']
    dynamic = Dynamic()
    if photo is not None:
        kind = filetype.guess(photo)
        if kind is None:
            return util.exception_response("")
        if kind.extension not in ['jpg', 'png', 'gif']:
            return util.exception_response(FILE_FORMAT_ERROR)
        file_path = os.path.join(settings.PHOTO_PATH, phone_number)
        fs = FileSystemStorage(location=file_path)
        file_name = 'photo.' + kind.extension
        new_name = fs.save(file_name, photo)
        dynamic.photo = new_name
    dynamic.phone_number = phone_number
    dynamic.text = text
    dynamic.save()

    return util.success_response()


class DynamicRes:
    id = int
    avatar = str
    text = str
    create_time = str
    user_name = str
    phone_number = str
    photo = str
    has_like = int
    like_count = int
    comment_count = int

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)


def dynamic_list(request):
    body = json.loads(request.body)
    limit = body.get('limit')
    offset = body.get('offset')
    phone_number = body.get('phone_number')
    dynamics = Dynamic.objects.filter(status=1).order_by("-id")[offset:limit]
    res = list()
    for dynamic in dynamics:
        user = UserInfo.objects.get(phone_number=dynamic.phone_number)
        user_name = user.user_name
        data = urllib.parse.urlencode({"phone_number": str(user.phone_number)})
        avatar = AVATAR_HOST + "?" + data
        try:
            has_like = Like.objects.get(dynamic_id=dynamic.id, operator=phone_number).status
        except Like.DoesNotExist:
            has_like = 0
        like_count = Like.objects.filter(dynamic_id=dynamic.id, status=1).count()
        comment_count = Comment.objects.filter(dynamic_id=dynamic.id, status=1).count()
        url = ""
        if dynamic.photo is not None:
            data = urllib.parse.urlencode({"id": str(dynamic.id)})
            url = PHOTO_HOST + "?" + data
        res.append(DynamicRes(id=dynamic.id, text=dynamic.text, avatar=avatar, photo=str(url),
                              create_time=str(dynamic.create_time), user_name=user_name,
                              phone_number=dynamic.phone_number, has_like=has_like, like_count=like_count,
                              comment_count=comment_count))

    return util.json_object_http_response(res)


def get_photo(request):
    id = request.GET['id']
    dynamic = Dynamic.objects.get(id=id)
    file_path = os.path.join(settings.PHOTO_PATH, dynamic.phone_number, dynamic.photo)
    try:
        file = open(file_path, 'rb')
    except FileNotFoundError:
        return util.exception_response(FILE_NOT_EXIST)
    return FileResponse(file)


def delete_dynamic(request):
    body = json.loads(request.body)
    id = body.get('id')
    dynamic = Dynamic.objects.get(id=id)
    dynamic.status = 0
    dynamic.save()
    return util.success_response()


def like_dynamic(request):
    body = json.loads(request.body)
    dynamic_id = body.get('id')
    operator = body.get('phone_number')
    try:
        like = Like.objects.get(dynamic_id=dynamic_id, operator=operator)
    except Like.DoesNotExist:
        like = Like(dynamic_id=dynamic_id, operator=operator, status=1)
        like.save()
        return util.success_response(status=1)
    like.status = not like.status
    like.save()
    return util.success_response(status=like.status)


def comment_dynamic(request):
    body = json.loads(request.body)
    dynamic_id = body.get('id')
    phone_number = body.get('phone_number')
    text = body.get('text')
    comment = Comment(operator=phone_number, text=text, dynamic_id=dynamic_id)
    comment.save()
    return util.success_response()


class CommentRes:
    id = int
    text = str
    create_time = str
    user_name = str
    phone_number = str

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)


def get_comment(request):
    body = json.loads(request.body)
    dynamic_id = body.get('id')
    comments = Comment.objects.filter(dynamic_id=dynamic_id, status=1)
    comment_list = list()
    for comment in comments:
        user_name = UserInfo.objects.get(phone_number=comment.operator).user_name
        comment_list.append(CommentRes(id=comment.id, text=comment.text,
                                       user_name=user_name,
                                       phone_number=comment.operator,
                                       create_time=str(comment.create_time)))
    return util.json_object_http_response(comment_list)
