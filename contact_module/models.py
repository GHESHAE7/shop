from django.db import models

# Create your models here.



class ContactUs(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='نام')
    email = models.CharField(max_length=255, null=False, blank=False, verbose_name='ایمیل')
    subject = models.CharField(max_length=255, null=False, blank=False, verbose_name='موصوغ')
    message = models.TextField(null=False, blank=False, verbose_name='پیام')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_active = models.BooleanField(default=True, null=False, verbose_name='فعال / غیر فعال')
    is_read_by_admin = models.BooleanField(default=False, verbose_name='خوانده شده توسط ادمین')
    
    
    def __str__(self):
        return self.name + '/' + self.email