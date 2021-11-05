from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name="post_detail"),
    path('accounts/signup/', views.Signup.as_view(), name="signup"),
    path('users/<int:pk>/', views.UserProfile.as_view(), name="profile"),
]
