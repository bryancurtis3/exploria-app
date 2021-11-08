from django.db.models import fields
from django.shortcuts import render, redirect

from django.views import View

from django.urls import reverse


from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView, UpdateView, FormView
from django.views.generic.detail import DetailView

from main_app.models import City, Post, User, Profile

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

class CityPost(TemplateView):
  model = City
  template_name = "city_posts.html"
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(self, **kwargs)
    context["posts"] = Post.objects.filter(location=self.name)

class PostDetail(DetailView):
  model = Post
  template_name = "post_detail.html"


class PostDelete(DeleteView):
  model = Post
  template_name = "post_delete_confirmation.html"
  # idk where to send this right now, so it's just going home for now
  success_url = "/"

class PostEdit(UpdateView):
  model = Post
  fields = ['img', 'description', 'location']
  template_name = "post_edit.html"

  def get_success_url(self):
    return reverse('post_detail', kwargs={'pk': self.object.pk})


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


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'image']

class UserProfile(DetailView):
  model = Profile
  template_name = "profile.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["posts"] = Post.objects.filter(user=self.object.pk)
    form = ProfileUpdateForm(instance=self.object)
    context["form"] = form
    return context
  
class ProfileUpdate(TemplateView):
  template_name = "user_update.html"
  
  def post(self, request, pk):
    form = ProfileUpdateForm(request.POST)
    if form.is_valid():
      Profile.objects.update(location=request.POST.get('location'), image=request.POST.get('image'), user=pk)
      return redirect("profile", pk=pk)
    else:
     context = {"form": form, "pk": pk}
     return render(request, "user_update.html", context)


class ProfileRedirect(View):
  def get(self, request):
    return redirect('profile', request.user.profile.pk)

class City(DetailView):
  model = City
  template_name = "city.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["posts"] = Post.objects.filter(city=self.object.pk)

    return context