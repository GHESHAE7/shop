from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Product, Category, Brand
from django.db.models import Max, Min
from django.utils import timezone
from datetime import timedelta
# Create your views here.



class ProductsListView(ListView):
    template_name = 'product_module/products.html'
    model = Product
    context_object_name = 'products'
    
    
    def get_queryset(self, *args, **kwargs):
        query = super().get_queryset(*args, **kwargs)
        query = query.filter(is_active=True).annotate(discount=Max('product_variant__discount')).order_by('-created_at')
        category_url = self.kwargs.get('category_url') or None
        brand_url = self.kwargs.get('brand_url') or None
        brnads = self.request.GET.getlist('brand')
        categories = self.request.GET.getlist('category')
        max_price = self.request.GET.get('max_price') or 0
        min_price = self.request.GET.get('min_price') or 0
        if category_url is not None:
            query = query.filter(category__url__exact=category_url)
        if brand_url is not None:
            query = query.filter(brand__url__exact=brand_url)
        if brnads:
            query = query.filter(brand__url__in=brnads)
        if categories:
            query = query.filter(category__url__in=categories)
        if min_price:
            query = query.filter(price__gte=min_price)
        if max_price:
            query = query.filter(price__lte=max_price)
        return query
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        old_time = timezone.now() - timedelta(7)
        categories = Category.objects.filter(is_active=True)
        brands = Brand.objects.filter(is_active=True)
        context['old_time'] = old_time
        context['categories'] = categories
        context['brands'] = brands
        context['checked_brands'] = self.request.GET.getlist('brand')
        context['checked_categories'] = self.request.GET.getlist('category')
        context['max_price'] = Product.objects.filter(is_active=True).aggregate(Max('price'))['price__max'] or 0
        context['min_price'] = Product.objects.filter(is_active=True).aggregate(Min('price'))['price__min'] or 0
        return context