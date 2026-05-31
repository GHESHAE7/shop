from django.shortcuts import render
from django.views import View
from account_module.models import User
from product_module.models import Brand, Category, Product, ProductVariant
from django.db.models import Count, Max, Sum, Avg, OuterRef, Subquery
from django.utils import timezone
from datetime import timedelta
from site_setting_module.models import Baner, Elan, SettingSite
from django.http import HttpRequest, HttpResponse
from cart_module.models import Order


class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        brands: Brand = Brand.objects.filter(is_active=True).order_by('?')
        categories: Category = Category.objects.filter(is_active=True).annotate(count_products=Count('products_category')).order_by('?')
        products_discount: Product = Product.objects.filter(is_active=True, product_variant__discount__isnull=False).annotate(discount=Max('product_variant__discount'), rating=Avg('comments__rating'))[:6]
        old_time = timezone.now() - timedelta(days=30)
        products_new: Product = Product.objects.filter(is_active=True, created_at__gte=old_time).annotate(discount=Max('product_variant__discount'), rating=Avg('comments__rating')).order_by('?')[:6]
        variant_sales = ProductVariant.objects.filter(product=OuterRef('pk')).values('product').annotate(total_sales=Sum('sales_count')).values('total_sales')
        products_sales_week = Product.objects.filter(is_active=True).annotate(sales_count=Subquery(variant_sales[:1]),discount=Max('product_variant__discount'),rating=Avg('comments__rating')).order_by('-sales_count')[:4]
        base_qs = Product.objects.filter(is_active=True)
        high_rating_products = (base_qs.annotate(rating=Avg('comments__rating'), max_discount=Max('product_variant__discount')).filter(rating__isnull=False).order_by('-rating').distinct()[:8])
        baners: Baner = Baner.objects.filter(is_active=True).order_by('-created_at')[:3]
     
        context = {
            'brands': brands,
            'categories': categories,
            'products_discount': products_discount,
            'products_new': products_new,
            'baners': baners,
            'products_sales_week': products_sales_week,
            'high_rating_products': high_rating_products,
        }
        
        try:
            elan_top: Elan = Elan.objects.get(is_active=True, where="top")
            context['elan_top'] = elan_top
        except Elan.DoesNotExist:
            pass
        
        try:
            elan_buttom: Elan = Elan.objects.get(is_active=True, where="buttom")
            context['elan_buttom'] = elan_buttom
        except Elan.DoesNotExist:
            pass

        return render(request, 'home_module/home.html', context)
    
    
    
def header_component(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.user.is_authenticated:
        try:
            user_id = request.user.id
            current_user: User = User.objects.get(id=user_id, is_active=True)
            site_setting = SettingSite.objects.get(is_active=True)
            count_order_item = Order.objects.filter(user_id=user_id, status='cart', is_active=True).aggregate(Count('order_items'))['order_items__count']
            context['user'] = current_user
            context['count_order_item'] = count_order_item
            context['site_setting'] = site_setting
            return render(request, "component_partial/header_component.html", context)
        except [User.DoesNotExist, Order.DoesNotExist, SettingSite.DoesNotExist]:
            return render(request, "component_partial/header_component.html", context)

    else:
        return render(request, "component_partial/header_component.html", context)



def footer_component(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "component_partial/footer_component.html", context)
