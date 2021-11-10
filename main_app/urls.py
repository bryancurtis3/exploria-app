from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('about/', views.About.as_view(), name="about"),
    path('accounts/signup/', views.Signup.as_view(), name="signup"),
    path('users/<int:pk>/', views.UserProfile.as_view(), name="profile"),
    path('users/<int:pk>/edit/', views.ProfileUpdate.as_view(), name="profile_update"),
    path('profile_redirect/', views.ProfileRedirect.as_view(), name="profile_redirect"),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name="post_detail"),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name="post_delete"),
    path('posts/<int:pk>/edit/', views.PostEdit.as_view(), name="post_edit"),
    path('posts/<int:pk>/comment/new/', views.CommentCreate.as_view(), name="comment_create"),
    path('posts/<int:pk>/comment/<int:comment_pk>/', views.CommentPostAssoc.as_view(), name="comment_post_assoc"),
    path('city/<int:pk>/', views.City.as_view(), name="city"),
    path('city/<int:pk>/posts/new/', views.PostCreate.as_view(), name="post_create"),
]