# -*- coding: utf-8 -*-
from datetime import datetime

from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework import serializers, exceptions

from oauth.models import ImageCaptcha
from drf_admin.utils.tools import decrypt_pass


class OauthSerializers(JSONWebTokenSerializer):

    def delete_captcha(self, instance):
        instance.delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["uuid"] = serializers.CharField(write_only=True, required=False)
        self.fields["captcha"] = serializers.CharField(write_only=True, required=False)

    def validate(self, attrs):
        uuid, captcha = attrs.pop("uuid", None), attrs.pop("captcha", None)
        if not all([uuid, captcha]):
            raise exceptions.ValidationError("请填写验证码")

        img_captcha = ImageCaptcha.objects.filter(uuid=uuid,
                                                  expire_time__gt=datetime.now()).first()

        if not img_captcha:
            raise exceptions.ValidationError('图片验证码已失效')

        if img_captcha.captcha.lower() != captcha.lower():
            self.delete_captcha(img_captcha)
            raise exceptions.ValidationError('图片验证码输入错误')

        self.delete_captcha(img_captcha)

        # 密码加密传输
        attrs["password"] = decrypt_pass(attrs.get("password"))

        return super(OauthSerializers, self).validate(attrs)
