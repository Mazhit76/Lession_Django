from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.utils.timezone import now


class User(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(
        blank=True, null=True, verbose_name='возраст')
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True
    #
    # def __str__(self):
    #     return self.username
