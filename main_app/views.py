from django.shortcuts import render, redirect

from django.views import View


from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from main_app.models import Post, User, Profile

# Auth imports
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

class Home(TemplateView):
  template_name = "home.html"


class PostDetail(DetailView):
  model = Post
  template_name = "post_detail.html"

  # def get_context_data(self, **kwargs):
  #   context = super().get_context_data(**kwargs)
  #   context["user"] = User.objects.
  #   return context

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

class UserProfile(DetailView):
  model = Profile
  template_name = "profile.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["posts"] = Post.objects.filter(user=self.object.pk)
    return context



