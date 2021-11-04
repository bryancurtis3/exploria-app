from django.shortcuts import render, redirect

from django.views import View


from django.views.generic.base import TemplateView

# Create your views here.

class Home(TemplateView):
    template_name = "home.html"

class PostDetail(TemplateView):
    template_name = "post_detail.html"