from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import check_username,generate_code
urlpatterns = [
     path('register/', TemplateView.as_view(template_name='register.html')),
     path('check_username/',check_username),
     path('generate_code/',generate_code),
]