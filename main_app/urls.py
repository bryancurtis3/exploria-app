from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('post/<int:pk>', views.PostDetail.as_view(), name="post_detail"),
]
