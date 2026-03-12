from django import template
from product_module.models import Product
from django.db.models import Max, Q
from django.utils import timezone
from datetime import timedelta



register = template.Library()


@register.filter
def res_discount(value, price):
    result = price - ((price / 100) * value)
    return int(result)



@register.inclusion_tag('product_module/inclusion/related_products.html')
def related_products_for_detail_page(brand):
    products = Product.objects.filter(is_active=True, brand__url=brand).annotate(discount=Max('product_variant__discount')).order_by('-created_at')
    old_time = timezone.now() - timedelta(7)

    return {
        'products': products,
        'old_time': old_time,
        'brand': brand,
    }