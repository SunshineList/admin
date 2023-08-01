# -*- coding: utf-8 -*-
import base64
import datetime
import json
import uuid

from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken

from captcha.image import ImageCaptcha as imagescaptcha

from oauth.models import ImageCaptcha
from drf_admin.apps.oauth.serializers.oauth_serializers import OauthSerializers
from drf_admin.utils.tools import random_valid_code

STAFF_IMAGE_CAPTCHA_LIFETIME = 5


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class ImageCaptchaView(APIView):
    """获取登录管理后台的图片验证码"""
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        image_uuid = uuid.uuid4()
        random_captcha = random_valid_code(4)

        image_captcha = imagescaptcha()
        byte_image = image_captcha.generate(random_captcha, format='JPEG').getvalue()

        ImageCaptcha.objects.create(
            is_active=True,
            uuid=image_uuid,
            captcha=random_captcha,
            expire_time=datetime.datetime.now() +
                        datetime.timedelta(minutes=STAFF_IMAGE_CAPTCHA_LIFETIME))
        return Response({
            'uuid': image_uuid,
            'image': 'data:image/jpeg;base64,%s' % base64.b64encode(byte_image).decode()
        })


class UserLoginView(ObtainJSONWebToken):
    """
    post:
    用户登录

    用户登录, status: 200(成功), return: Token信息
    """
    throttle_classes = [AnonRateThrottle]
    serializer_class = OauthSerializers

    def post(self, request, *args, **kwargs):
        # 重写父类方法, 定义响应字段内容
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            conn = get_redis_connection('user_info')
            conn.incr('visits')
            return response
        else:
            if response.data.get('non_field_errors'):
                # 日后将增加用户多次登录错误,账户锁定功能(待完善)
                if isinstance(response.data.get('non_field_errors'), list) and len(
                        response.data.get('non_field_errors')) > 0:
                    if response.data.get('non_field_errors')[0].strip() == '无法使用提供的认证信息登录。':
                        return Response(data={'detail': '用户名或密码错误'}, status=status.HTTP_400_BAD_REQUEST)
            raise ValidationError(response.data)


class UserInfoView(APIView):
    """
    get:
    当前用户信息

    当前用户信息, status: 200(成功), return: 用户信息和权限
    """

    def get(self, request):
        user_info = request.user.get_user_info()
        # 将用户信息缓存到redis
        conn = get_redis_connection('user_info')
        if request.user.is_superuser and 'admin' not in user_info['permissions']:
            user_info['permissions'].append('admin')
        user_info['permissions'] = json.dumps(user_info['permissions'])
        user_info['avatar'] = request._current_scheme_host + user_info.get('avatar')
        conn.hmset('user_info_%s' % request.user.id, user_info)
        conn.expire('user_info_%s' % request.user.id, 60 * 60 * 24)  # 设置过期时间为1天
        user_info['permissions'] = json.loads(user_info['permissions'])
        return Response(user_info, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    """
    post:
    退出登录

    退出登录, status: 200(成功), return: None
    """

    def post(self, request):
        content = {}
        # 后续将增加redis token黑名单功能
        return Response(data=content)
