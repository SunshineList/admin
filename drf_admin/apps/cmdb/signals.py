# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save
from django.dispatch import receiver

from cmdb.models import Accounts


@receiver(pre_save, sender=Accounts)
def encrypt_password_accounts(sender, instance, **kwargs):
    """
    保存服务器登录账户时将密码加密存储
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    instance.set_password('password', instance.password)
