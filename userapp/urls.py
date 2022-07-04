from django.urls import path
from knox import views as knox_views

from userapp.views import *


urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='user_register'),
    path('login/', LoginAPI.as_view(), name='user_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),

]