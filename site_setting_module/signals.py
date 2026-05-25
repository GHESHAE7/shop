from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import SettingSite
import os

@receiver(post_delete, sender=SettingSite)
def delete_logo_on_site_setting(sender, instance, **kwargs):
    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)