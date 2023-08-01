from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token

from oauth.views import auth, home

urlpatterns = [
    path('home/', home.HomeAPIView.as_view()),
    path('login/', auth.UserLoginView.as_view()),
    path('logout/', auth.LogoutAPIView.as_view()),
    path('refresh/', refresh_jwt_token),
    path('info/', auth.UserInfoView.as_view()),
    path('captcha/', auth.ImageCaptchaView.as_view()),
]
