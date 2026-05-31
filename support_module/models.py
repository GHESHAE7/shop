from django.db import models


class SupportCategory(models.Model):
    name = models.CharField(
        max_length=200, null=False, blank=False, verbose_name="دسته بندی"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین آپدیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(
        default=True, null=False, verbose_name="فعال / غیر فعال"
    )

    def __str__(self):
        return self.name


class Support(models.Model):
    name = models.CharField(max_length=500, null=False, blank=False, verbose_name="نام")
    description = models.TextField(null=False, blank=False, verbose_name="توضیحات")
    categpry = models.ForeignKey(
        SupportCategory,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="دسته بندی",
        related_name="supports",
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین آپدیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(
        default=True, null=False, verbose_name="فعال / غیر فعال"
    )

    def __str__(self):
        return self.name
