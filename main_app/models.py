from django.db import models

from django.db.models import Model

from django.contrib.auth.models import User
from django.db.models.fields import CharField, TextField
from django.db.models.fields.related import ForeignKey

# Create your models here.

# class User(Model):

class Post(Model):
  title = CharField(max_length=100)
  img = CharField(max_length=250)
  description = TextField(max_length=4000)
  # Possibly created_at, but client didn't ask

  user = ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self) -> str:
    return self.title