# -*- coding: utf-8 -*-
from django.urls import path, include

from drf_admin.apps.cmdb.views import servers, assets
from drf_admin.utils import routers

router = routers.AdminRouter()
router.register(r'servers', servers.ServersViewSet, basename="servers")  # 服务器管理
urlpatterns = [
    path('servers/system-type/', servers.ServersSystemTypeAPIView.as_view()),
    path('servers/type/', servers.ServersTypeAPIView.as_view()),
    path('assets/status/', assets.AssetsStatusAPIView.as_view()),
    path('assets/admin/', assets.AssetsAdminListAPIView.as_view()),
    path('assets/cabinets/', assets.IDCCabinetsTreeAPIView.as_view()),
    path('', include(router.urls)),
]
