from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('postdetail/', views.PostDetail.as_view(), name="post_detail"),
    path('accounts/signup/', views.Signup.as_view(), name="signup"),
]
