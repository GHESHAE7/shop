from django.shortcuts import render
from django.views import View
from account_module.models import User
from product_module.models import Brand, Category, Product, ProductVariant
from django.db.models import Count, Max, Sum, Avg, OuterRef, Subquery
from django.utils import timezone
from datetime import timedelta
from site_setting_module.models import Baner, Elan
from django.http import HttpRequest, HttpResponse
from cart_module.models import Order
# Create your views here.


class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        brands: Brand = Brand.objects.filter(is_active=True).values('name', 'url', 'image')
        categories: Category = Category.objects.filter(is_active=True).annotate(count_products=Count('products_category')).values('name', 'url', 'image', 'count_products')
        products_discount: Product = Product.objects.filter(is_active=True, product_variant__discount__isnull=False).annotate(discount=Max('product_variant__discount'))[:8]
        # old_time = timezone.now() - timedelta(days=7)
        # products_new: Product = Product.objects.filter(is_active=True, created_at__gte=old_time).annotate(discount=Max('product_variant__discount'))[:8]
        products_new: Product = Product.objects.filter(is_active=True,).annotate(discount=Max('product_variant__discount')).order_by('-created_at')[:8]
        variant_sales = (ProductVariant.objects.filter(product=OuterRef('pk')).values('product').annotate(total_sales=Sum('sales_count')).values('total_sales'))
        products_sales_week = (Product.objects.filter(is_active=True).annotate(sales_count=Subquery(variant_sales[:1]),discount=Max('product_variant__discount'),rating=Avg('comments__rating')).order_by('-sales_count'))[:4]
        baners: Baner = Baner.objects.filter(is_active=True).order_by('-created_at')[:3]
        elan_top: Elan = Elan.objects.filter(is_active=True, where="top")[0] or 0
        elan_buttom: Elan = Elan.objects.filter(is_active=True, where="buttom")[0] or 0
        context = {
            'brands': brands,
            'categories': categories,
            'products_discount': products_discount,
            'products_new': products_new,
            'baners': baners,
            'elan_top': elan_top,
            'elan_buttom': elan_buttom,
            'products_sales_week': products_sales_week,
        }
        return render(request, 'home_module/home.html', context)
    
    
    
def header_component(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        user_id = request.user.id
        current_user: User = User.objects.filter(id=user_id, is_active=True).first()
        count_order_item = Order.objects.filter(user_id=user_id, status='cart', is_active=True).aggregate(Count('order_items'))['order_items__count']
        context = {
            'user': current_user,
            'count_order_item': count_order_item,
        }
        return render(request, "component_partial/header_component.html", context)
    else:
        context = {}
        return render(request, "component_partial/header_component.html", context)



def footer_component(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "component_partial/footer_component.html", context)