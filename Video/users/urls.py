from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from .views import check_username,generate_code,verify_code,submit_register,submit_login
from . import views
urlpatterns = [
     path('register/', TemplateView.as_view(template_name='register.html')),
     path('login/', TemplateView.as_view(template_name='login.html')),
     path('check_username/',check_username),
     path('generate_code/',generate_code),
     path('verify_code/',verify_code),
     path('submit_register/',submit_register),
     path('submit_login/',submit_login),
     re_path(r'^logout/$', views.logout),
     re_path(r'^user_info/$', views.UserInfoView.as_view()),
     re_path(r'^list_user/$', views.UserListView.as_view()),
     re_path(r'^add_focus/$', views.add_focus),
     re_path(r'^my_focus/$', views.my_focus),

]