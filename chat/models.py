from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=None, null=True)
    text = models.TextField()
    watched = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}: {self.text}'


class Room(models.Model):
    title = models.CharField(max_length=40, blank=True, verbose_name="Назва чату")
    users = models.ManyToManyField(User, blank=True, default=None)
    slug = models.SlugField()
    message = models.ManyToManyField(Message)

    def __str__(self):
        users = [login.username for login in self.users.all()]

        return f'Назва: {self.title}  Користувачі: [{", ".join(users)}]'
