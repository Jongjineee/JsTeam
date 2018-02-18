from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from sorl.thumbnail import ImageField

# Create your models here.

def user_path(instance, filename):
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr)
    extension = filename.split('.')[-1]
    return '%s/%s.%s' % (instance.owner.username, pid, extension)


class Photo(models.Model):
    image = ImageField(upload_to = user_path)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)
    title = models.CharField(max_length = 255, default='')
    pub_date = models.DateTimeField(auto_now_add = True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return '{} {} {}'.format(self.owner.username, self.title, self.is_public)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)
    nickname = models.CharField(max_length = 64)
    profile_photo = models.ImageField(blank=True)


class Comment(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} by {}'.format(self.message, self.author)

