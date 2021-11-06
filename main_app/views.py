from django.db.models import fields
from django.shortcuts import render, redirect

from django.views import View

from django.urls import reverse


from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, FormView
from django.views.generic.detail import DetailView

from main_app.models import Post, User, Profile

from django.forms import ModelForm

# Auth imports
from django.contrib.auth import login
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm


# Create your views here.

class Home(TemplateView):
  template_name = "home.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["signup_form"] = UserCreationForm()
    context["login_form"] = AuthenticationForm()
    return context


class PostDetail(DetailView):
  model = Post
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
          Profile.objects.create(location=request.POST.get('location'), user=user)
          # Profile.objects.create(email=request.POST.get('email'), user=user)
          # Profile.objects.create(first_name=request.POST.get('first_name'), user=user)
          # Profile.objects.create(last_name=request.POST.get('last_name'), user=user)
          login(request, user)
          return redirect("profile_redirect")
      else:
          context = {"form": form}
          return render(request, "registration/signup.html", context) # FIXME - if invalid form input, how to redirect back to modal form? Currently redirecting to unused signup page


class UserProfile(DetailView):
  #model = User
  model = Profile
  template_name = "profile.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # context["profile"] = Profile.objects.filter(user_id=self.object.pk)
    context["posts"] = Post.objects.filter(user=self.object.pk)
    context["update_form"] = UserChangeForm()
    return context

class ProfileUpdate(TemplateView):
  template_name = "user_update.html"

  def get(self, request):
    form = UserChangeForm()
    context = {"form" : form}
    return render(request, "user_update.html", context)
  
  def post(self, request):
    form = UserChangeForm(request.POST)
    if form.is_valid():
      user = form.save()
      Profile.objects.update()
      return redirect("profile")
    else:
      context = {"form": form}
      return render(request, "user_update.html", context)

# class ProfileUpdate(TemplateView):
#   template_name = "profile.html"
#   fields = ['location', 'image']

#   def get_context_data(self, **kwargs):
#       context = super(ProfileUpdate, self).get_context_data(**kwargs)
#       context['User'] = User.objects.get(pk=self.object.pk)
#       return context
  
#   # Not sure if this is how the success url is supposed to be looking
#   def get_success_url(self):
#     return reverse('profile', kwargs={'pk': self.object.pk})

#   def form_valid(self, form):

#     user_id = Profile.objects.get(pk=self.object.pk).user.pk
#     User.objects.filter(pk=user_id).update(username=self.request.POST.get('username'))

#     return super(ProfileUpdate, self).form_valid(form)


class ProfileRedirect(View):
  def get(self, request):
    return redirect('profile', request.user.profile.pk)
