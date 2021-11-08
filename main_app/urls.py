from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name="post_detail"),
    path('accounts/signup/', views.Signup.as_view(), name="signup"),
    path('users/<int:pk>/', views.UserProfile.as_view(), name="profile"),
    path('users/<int:pk>/edit/', views.ProfileUpdate.as_view(), name="profile_update"),
    path('profile_redirect', views.ProfileRedirect.as_view(), name="profile_redirect"),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name="post_delete"),
    path('posts/<int:pk>/edit/', views.PostEdit.as_view(), name="post_edit"),
]
