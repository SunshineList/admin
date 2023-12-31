# -*- coding: utf-8 -*-
from easyaudit.models import CRUDEvent
from rest_framework.generics import ListAPIView

from drf_admin.apps.monitor.serializers.crud import CRUDSerializer


class CRUDListAPIView(ListAPIView):
    """
    get:
    监控--CRUD变更记录列表

    CRUD变更记录列表, status: 200(成功), return: CRUD变更记录列表信息
    """
    serializer_class = CRUDSerializer

    def get_queryset(self):
        return CRUDEvent.objects.exclude(object_repr__istartswith='OnlineUsers')
