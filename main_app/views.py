from django.shortcuts import render, redirect

from django.views import View


from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from main_app.models import Post

# Create your views here.

class Home(TemplateView):
  template_name = "home.html"

class PostDetail(DetailView):
  model = Post
  template_name = "post_detail.html"