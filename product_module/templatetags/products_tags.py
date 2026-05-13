from django import template
from product_module.models import Product
from django.db.models import Max, Q, Avg
from django.utils import timezone
from datetime import timedelta



register = template.Library()


@register.filter
def res_discount(value, price):
    result = price - ((price / 100) * value)
    return int(result)



@register.inclusion_tag('product_module/inclusion/related_products.html')
def related_products_for_detail_page(brand, category):
    products = Product.objects.filter(is_active=True).annotate(discount=Max('product_variant__discount'), rating=Avg('comments__rating')).order_by('?')
    products = products.filter(Q(brand__url=brand) | Q(category__url=category))[:8]
    old_time = timezone.now() - timedelta(7)
    print(category)
    return {
        'products': products,
        'old_time': old_time,
        'brand': brand,
    }
    
    

@register.inclusion_tag('product_module/inclusion/show_rating_products.html')
def show_rating_products(rating):
    return {
        'rating': rating,
    }