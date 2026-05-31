from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Product, ManyImages
from pathlib import Path


@receiver(post_delete, sender=Product)
def delete_image_on_product(sender, instance, **kwargs):
    if instance.image:
        path = Path(instance.image.path)
        if path.is_file():
            path.unlink()


@receiver(post_delete, sender=ManyImages)
def delete_image_on_many_image(sender, instance, **kwargs):
    if instance.image:
        path = Path(instance.image.path)
        if path.is_file():
            path.unlink()
