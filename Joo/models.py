from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models


class Admin(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=100)
    publication_date = models.DateField()
    publisher = models.ForeignKey(Admin, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    in_active = models.BooleanField(null=True)
    creator_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post_image = models.ImageField(null=True, blank=True, upload_to='images/')
    num_visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(blank=True, null=True)


class Comment(models.Model):
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(null=True)
    creator_id = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.post.description, self.content)
