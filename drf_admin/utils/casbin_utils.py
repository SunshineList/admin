# -*- coding: utf-8 -*-
import os.path
import casbin

from django.core.exceptions import PermissionDenied

from drf_admin.settings.dev import BASE_DIR


class CasbinMiddleware:
    """
    Casbin middleware.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.enforcer = casbin.Enforcer(os.path.join(BASE_DIR, "apps", "user_casbin", "casbin_model.conf"),
                                        os.path.join(BASE_DIR, "apps", "user_casbin", "casbin_policy.csv"))

    def __call__(self, request):
        if not self.check_permission(request):
            self.require_permission()

        response = self.get_response(request)
        return response

    def check_permission(self, request):
        # Customize it based on your authentication method.
        user = request.user.username
        if request.user.is_anonymous:
            user = 'anonymous'
        path = request.path
        method = request.method
        return self.enforcer.enforce(user, path, method)

    def require_permission(self):
        raise PermissionDenied


a = CasbinMiddleware({})
