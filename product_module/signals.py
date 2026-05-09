from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Product, ManyImages
import os

@receiver(post_delete, sender=Product)
def delete_image_on_product(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)



@receiver(post_delete, sender=ManyImages)
def delete_image_on_many_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)