from django.http import HttpResponse, FileResponse
import json
from user.models import *
import traceback
import filetype
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
import util

REGISTER_FAIL = "注册失败"
LOGIN_FAIL = "登录失败"
FILE_FORMAT_ERROR = "图片文件格式错误"
USER_NOT_EXIST = "不存在该用户"
FILE_NOT_EXIST = "不存在头像文件"
PHONE_NUMBER_EXIST = "该手机号码已注册"


def register(request):
    body = json.loads(request.body)
    user_info = UserInfo()
    user_info.user_name = body.get("user_name")
    user_info.password = body.get("password")
    user_info.phone_number = body.get("phone_number")
    exist = UserInfo.objects.filter(phone_number=user_info.phone_number)
    if len(exist) != 0:
        return util.exception_response(PHONE_NUMBER_EXIST)
    try:
        user_info.save()
    except ValueError or KeyError:
        print(traceback)
        return util.exception_response(REGISTER_FAIL)
    return util.success_response()


def login(request):
    body = json.loads(request.body)
    user_info = UserInfo()
    user_info.phone_number = body.get("phone_number")
    user_info.password = body.get("password")
    success = user_info.verify()
    if success:
        return util.success_response()
    else:
        return util.exception_response(LOGIN_FAIL)


def upload_avatar(request):
    phone_number = request.POST['phone_number']
    avatar = request.FILES.get('avatar')
    kind = filetype.guess(avatar)
    if kind is None:
        return util.exception_response("")
    if kind.extension not in ['jpg', 'png', 'gif']:
        return util.exception_response(FILE_FORMAT_ERROR)

    fs = FileSystemStorage(location=settings.AVATAR_PATH)
    file_name = 'avatar.' + kind.extension
    new_name = fs.save(file_name, avatar)
    try:
        UserInfo.objects.get(phone_number=phone_number)
        UserInfo.objects.filter(phone_number=phone_number).update(avatar=new_name)
    except UserInfo.DoesNotExist:
        return util.exception_response(USER_NOT_EXIST)
    return util.success_response()


def get_avatar(request):
    phone_number = request.GET['phone_number']
    try:
        user_info = UserInfo.objects.get(phone_number=phone_number)
    except UserInfo.DoesNotExist:
        return util.exception_response(USER_NOT_EXIST)
    file_path = os.path.join(settings.AVATAR_PATH, user_info.avatar)
    try:
        file = open(file_path, 'rb')
    except FileNotFoundError:
        return util.exception_response(FILE_NOT_EXIST)
    return FileResponse(file)
