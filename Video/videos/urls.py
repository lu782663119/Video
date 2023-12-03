from django.urls import path, include,re_path
from django.views.generic import TemplateView
from . import views
urlpatterns = [
    path('index/', views.index),
    path('upload/', TemplateView.as_view(template_name='upload.html')),
    path('upload_video/',views.VideosView.as_view()),
    re_path(r'^vid/(?P<operator>.*)$',views.VideoListView.as_view()),
    re_path(r'^play_video/$', views.play_video),
    re_path(r'^delete_video/$', views.delete_video),


]