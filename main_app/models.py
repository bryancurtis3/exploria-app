from typing import Mapping
from django.db import models

from django.db.models import Model

from django.contrib.auth.models import User
from django.db.models.fields import CharField, TextField
from django.db.models.fields.related import ForeignKey

# Create your models here.

# class User(Model) extends the User model to include additional attributes:
class Profile(Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  location = models.CharField(max_length=100)
  image = models.CharField(max_length=300, default="https://media.istockphoto.com/vectors/all-seeing-eye-icon-eye-in-triangle-illuminati-mason-symbol-vector-vector-id1265037182?k=20&m=1265037182&s=170667a&w=0&h=lZ4GKha5J9UNqLsIilcKSzQgrn8cm_teitVKYXlxW_w=")


class City(Model):
  name = CharField(max_length=100)
  img = CharField(max_length=300)

  def __str__(self) -> str:
    return self.name

class Post(Model):
  title = CharField(max_length=200)
  img = CharField(max_length=250)
  description = TextField(max_length=4000)
  location = CharField(max_length=50, default="San Francisco")

  user = ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
  city = ForeignKey(City, on_delete=models.CASCADE, related_name="posts")

  def __str__(self) -> str:
    return self.title