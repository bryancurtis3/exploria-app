from django.shortcuts import render, redirect

from django.views import View


from django.views.generic.base import TemplateView

# Auth imports
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

class Home(TemplateView):
  template_name = "home.html"

class PostDetail(TemplateView):
  template_name = "post_detail.html"

class Signup(TemplateView):
  template_name = "signup.html"

  def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)
    
  def post(self, request):
      form = UserCreationForm(request.POST)
      if form.is_valid():
          user = form.save()
          login(request, user)
          return redirect("/")
      else:
          context = {"form": form}
          return render(request, "registration/signup.html", context)

