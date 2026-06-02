from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from pathlib import Path
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(
        max_length=90,
        null=False,
        blank=False,
        verbose_name="نام دسته بندی",
        unique=True,
    )
    url = models.CharField(
        max_length=120,
        null=False,
        blank=False,
        verbose_name="نام دسته بندی در url",
        unique=True,
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="توضیحات دسته بندی"
    )
    image = models.ImageField(upload_to="category/image", null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین آپدیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(
        default=True, null=False, verbose_name="فعال / غیر فعال"
    )

    def get_absolute_url(self):
        return reverse(
            "product_module:products_by_category_page",
            kwargs={"category_url": self.url},
        )

    def save(self, *args, **kwargs):
        old_image_path = None

        if self.pk:
            try:
                old = Category.objects.get(pk=self.pk)
                if old.image and old.image != self.image:
                    old_image_path = Path(old.image.path)

            except Category.DoesNotExist:
                pass
        super(Category, self).save(*args, **kwargs)

        if old_image_path and old_image_path.is_file():
            old_image_path.unlink()

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(
        max_length=90, null=False, blank=False, verbose_name="نام برند", unique=True
    )
    url = models.CharField(
        max_length=120,
        null=False,
        blank=False,
        verbose_name="نام برند در url",
        unique=True,
    )
    description = models.TextField(null=True, blank=True, verbose_name="توضیحات برند")
    image = models.ImageField(upload_to="brand/image", null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین آپدیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(
        default=True, null=False, verbose_name="فعال / غیر فعال"
    )

    def get_absolute_url(self):
        return reverse(
            "product_module:products_by_brand_page", kwargs={"brand_url": self.url}
        )

    def save(self, *args, **kwargs):
        old_image_path = None

        if self.pk:
            try:
                old = Brand.objects.get(pk=self.pk)
                if old.image and old.image != self.image:
                    old_image_path = Path(old.image.path)

            except Brand.DoesNotExist:
                pass
        super(Brand, self).save(*args, **kwargs)

        if old_image_path and old_image_path.is_file():
            old_image_path.unlink()

    def __str__(self):
        return self.name


class Product(models.Model):
    class ChoicesGender(models.TextChoices):
        man = "man", _("Man")
        woman = "women", _("Women")
        both = "both", _("Both")

    name = models.CharField(
        max_length=255, null=False, blank=False, verbose_name="نام محصول"
    )
    category = models.ForeignKey(
        Category,
        verbose_name="دسته بندی محصول",
        related_name="products_category",
        on_delete=models.SET_NULL,
        null=True,
    )
    brand = models.ForeignKey(
        Brand,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="برند محصول",
        related_name="products_brand",
    )
    price = models.BigIntegerField(null=False, blank=False, verbose_name="قیمت محصول")
    description = models.TextField(
        verbose_name="توضیحات محصول", null=False, blank=False
    )
    gender = models.CharField(
        choices=ChoicesGender,
        null=False,
        blank=False,
        max_length=20,
    )
    image = models.ImageField(upload_to="product/image", null=False, blank=False)
    slug = models.SlugField(max_length=255, null=False, blank=False, unique=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین آپدیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(
        default=True, null=False, verbose_name="فعال / غیر فعال"
    )

    def get_absolute_url(self):
        return reverse("product_module:product_detail_page", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        old_image_path = None

        if self.pk:
            try:
                old = Product.objects.get(pk=self.pk)
                if old.image and old.image != self.image:
                    old_image_path = Path(old.image.path)

            except Product.DoesNotExist:
                pass
        super(Product, self).save(*args, **kwargs)

        if old_image_path and old_image_path.is_file():
            old_image_path.unlink()

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, null=True, on_delete=models.SET_NULL, related_name="product_variant"
    )
    color = models.CharField(
        max_length=120, null=False, blank=False, verbose_name="رنگ"
    )
    size = models.CharField(max_length=20, null=False, blank=False, verbose_name="سایز")
    stock = models.IntegerField(default=0, null=False, blank=False)
    discount = models.PositiveSmallIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    sales_count = models.IntegerField(default=0, verbose_name="تعداد به فروش رفته")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین آپدیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(
        default=True, null=False, verbose_name="فعال / غیر فعال"
    )

    def __str__(self):
        return self.product.name


class ManyImages(models.Model):
    image = models.ImageField(upload_to="product/image", null=True, blank=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="product_images",
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین آپدیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(
        default=True, null=False, verbose_name="فعال / غیر فعال"
    )

    def save(self, *args, **kwargs):
        old_image_path = None

        if self.pk:
            try:
                old = ManyImages.objects.get(pk=self.pk)
                if old.image and old.image != self.image:
                    old_image_path = Path(old.image.path)

            except ManyImages.DoesNotExist:
                pass
        super(ManyImages, self).save(*args, **kwargs)

        if old_image_path and old_image_path.is_file():
            old_image_path.unlink()

    def __str__(self):
        return self.product.name
