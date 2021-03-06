from django.db.models import fields
from django.shortcuts import render, redirect

from django.views import View

from django.urls import reverse

from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView, UpdateView, FormView, CreateView
from django.views.generic.detail import DetailView

from main_app.models import Post, User, Profile, Comment
from main_app.models import City as CityModel

from django.forms import ModelForm

# Authentication imports
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Authorization imports
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.

class Home(TemplateView):
  template_name = "home.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["signup_form"] = UserCreationForm()
    context["login_form"] = AuthenticationForm()
    return context

class About(TemplateView):
  template_name = "about.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["signup_form"] = UserCreationForm()
    context["login_form"] = AuthenticationForm()
    return context

class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

@method_decorator(login_required, name='dispatch')
class PostDetail(DetailView):
  model = Post
  template_name = "post_detail.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["cities"] = CityModel.objects.order_by('name')
    form = CommentCreateForm()
    context["form"] = form
    return context

@method_decorator(login_required, name='dispatch')
class PostDelete(DeleteView):
  model = Post
  template_name = "post_delete_confirmation.html"

  def get_success_url(self):
    return reverse('city', kwargs={'pk': self.object.city.pk})

@method_decorator(login_required, name='dispatch')
class PostEdit(UpdateView):
  model = Post
  fields = ['title', 'img', 'description']
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
          login(request, user)
          return redirect("profile_redirect")
      else:
          context = {"form": form}
          return render(request, "registration/signup.html", context) # FIXME - if invalid form input, how to redirect back to modal form? Currently redirecting to unused signup page

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'image']

@method_decorator(login_required, name='dispatch')
class UserProfile(DetailView):
  model = Profile
  template_name = "profile.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    form = ProfileUpdateForm(instance=self.object)
    context["form"] = form
    return context
  
@method_decorator(login_required, name='dispatch')
class ProfileUpdate(View):
  
  def post(self, request, pk):
    form = ProfileUpdateForm(request.POST)
    if form.is_valid():
      Profile.objects.filter(user=pk).update(location=request.POST.get('location'), image=request.POST.get('image'))
      return redirect("profile", pk=pk)
    else:
      context = {"form": form, "pk": pk}
      return render(request, "profile.html", context)

@method_decorator(login_required, name='dispatch')
class ProfileRedirect(View):
  def get(self, request):
    return redirect('profile', request.user.profile.pk)

class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'img', 'description']

@method_decorator(login_required, name='dispatch')
class City(DetailView):
  model = CityModel
  template_name = "city.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["cities"] = CityModel.objects.order_by('name')
    form = PostCreateForm()
    context["form"] = form
    return context

@method_decorator(login_required, name='dispatch')
class PostCreate(View):
  def post(self, request, pk):
    title = request.POST.get("title")
    img = request.POST.get("img")
    description = request.POST.get('description')
    city = CityModel.objects.get(pk=pk)
    location = city.name
    
    Post.objects.create(title=title, img=img, description=description, location=location, city=city, user=request.user)
    return redirect("city", pk=pk) 

@method_decorator(login_required, name='dispatch')
class CommentCreate(View):
  def post(self, request, pk):
    content = request.POST.get("content")
    post = Post.objects.get(pk=pk)
    
    Comment.objects.create(content=content, post=post, user=request.user)
    return redirect("post_detail", pk=pk) 

@method_decorator(login_required, name='dispatch')
class CommentPostAssoc(View):
  def get(self, request, pk, comment_pk):
    assoc = request.GET.get("assoc")
    if assoc == "remove":
      Comment.objects.filter(id=comment_pk).delete()
    return redirect('post_detail', pk)