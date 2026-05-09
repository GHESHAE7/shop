from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
import os
# Create your models here.


class User(AbstractUser):
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن', null=True, blank=True)
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    avatra = models.ImageField(null=True, blank=True, upload_to='users/avatar', verbose_name='عکس')
    email_active_code = models.CharField(max_length=126, null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        old_image_path = None
        
        if self.pk:
            try:
                old = User.objects.get(pk=self.pk)
                if old.image and old.image != self.image:
                    old_image_path = old.image.path
                
            except User.DoesNotExist:
                pass
        super(User, self).save(*args, **kwargs)
        
        if old_image_path and os.path.isfile(old_image_path):
            os.remove(old_image_path)