from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse

SCORE_CHOICES = (
    (10, 10),
    (20, 20),
    (30, 30),
    (40, 40),
    (50, 50),
    (60, 60),
    (70, 70),
    (80, 80),
    (90, 90),
    (100, 100),
 )

class Product(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField()
    created_at = models.DateTimeField(default=datetime.now, blank=True)


class Flag(models.Model):
    q1 = models.IntegerField(max_length=200, blank=True)
    h1 = models.TextField(max_length=5000, blank=True)
    f1 = models.CharField(max_length=200, blank=True)
    score = models.IntegerField(choices = SCORE_CHOICES, blank=True, default= 10)

class Flags(models.Model):
    q1 = models.IntegerField(max_length=200, blank=True, default=1)
    quest = models.ForeignKey(Product, on_delete=models.CASCADE)
    h1 = models.CharField(max_length=2000, blank=True)
    image = models.ImageField(upload_to='uploads/',null=True, blank=True)
    f1 = models.CharField(max_length=200, blank=True)
    score = models.IntegerField(choices = SCORE_CHOICES, blank=True, default= 10)

class complete(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hint = models.ForeignKey(Flags, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    finished_at = models.DateTimeField(default=datetime.now)

class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    finished_at = models.DateTimeField(blank=True, default=datetime.now)

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flag = models.ForeignKey(Flags, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)

class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flag = models.ForeignKey(Flags, on_delete=models.CASCADE)
    attempt = models.IntegerField(default=0)

class Scene(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hecker = models.IntegerField(default=0)

def __str__(self):
    return self.name

def get_absolute_url(self):
    return reverse('index')