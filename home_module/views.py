from django.shortcuts import render
from django.views import View
from account_module.models import User
from product_module.models import Brand, Category, Product
from django.db.models import Count, Max
from django.utils import timezone
from datetime import timedelta
from site_setting_module.models import Baner
# Create your views here.


class HomeView(View):
    def get(self, request):
        brands = Brand.objects.filter(is_active=True).values('name', 'url', 'image')
        categories = Category.objects.filter(is_active=True).annotate(count_products=Count('products_category')).values('name', 'url', 'image', 'count_products')
        products_discount = Product.objects.filter(is_active=True, product_variant__discount__isnull=False).annotate(discount=Max('product_variant__discount'))[:8]
        old_time = timezone.now() - timedelta(days=7)
        products_new = Product.objects.filter(is_active=True, created_at__gte=old_time).annotate(discount=Max('product_variant__discount'))[:8]
        baners = Baner.objects.filter(is_active=True).order_by('-created_at')[:3]
        context = {
            'brands': brands,
            'categories': categories,
            'products_discount': products_discount,
            'products_new': products_new,
            'baners': baners,
        }
        return render(request, 'home_module/home.html', context)
    
    def post(self, request):
        pass
    
    
def header_component(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        current_user = User.objects.filter(id=user_id, is_active=True).first()
        context = {
            'user': current_user
        }
        return render(request, "component_partial/header_component.html", context)
    else:
        context = {}
        return render(request, "component_partial/header_component.html", context)


def footer_component(request):
    context = {}
    return render(request, "component_partial/footer_component.html", context)