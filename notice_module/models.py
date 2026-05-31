from django.db import models
from account_module.models import User

# Create your models here.


class Notice(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True, verbose_name="هدر")
    message = models.TextField(null=False, blank=False, verbose_name="متن اعلان")
    icon = models.CharField(
        null=True, blank=True, default="fa-bell", verbose_name="ایکون اعلان"
    )
    user = models.ManyToManyField(User, blank=True, verbose_name="برای کدام کاربران")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین آپدیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(
        default=True, null=False, verbose_name="فعال / غیر فعال"
    )

    def __str__(self):
        return self.title
