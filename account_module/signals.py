from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import User
import os

@receiver(post_delete, sender=User)
def delete_image_on_user(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)