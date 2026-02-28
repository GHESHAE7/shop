from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
# Create your models here.


class User(AbstractUser):
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن', null=True, blank=True)
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    avatra = models.ImageField(null=True, blank=True, upload_to='users/avatar', verbose_name='عکس')
    email_active_code = models.CharField(max_length=126, null=True, blank=True)