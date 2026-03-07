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
        discounted = self.request.GET.get('discounted')
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
        if discounted:
            query = query.filter(product_variant__discount__gt=0)
        if min_price:
            query = query.filter(price__gte=min_price)
        if max_price:
            query = query.filter(price__lte=max_price)
        if self.request.path.endswith('/discount'):
            query = query.filter(product_variant__discount__gt=0)
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
        context['checked_discounted'] = self.request.GET.get('discounted')
        context['max_price'] = Product.objects.filter(is_active=True).aggregate(Max('price'))['price__max'] or 0
        context['min_price'] = Product.objects.filter(is_active=True).aggregate(Min('price'))['price__min'] or 0
        
        if self.request.path.endswith(''):
            context['title_heading'] = 'محصولات'
            context['title'] = 'تمام محصولات فروشگاه'
            context['show_discount'] = True
            
            
        if self.request.path.endswith('/discount'):
            context['title_heading'] = 'محصولات تخفیف دار'
            context['title'] = 'تمام محصولات تخفیف دار'
            context['show_discount'] = False
            
            
        if '/category/' in self.request.path:
            category_url = self.kwargs.get('category_url')
            context['title_heading'] = f'دسته بندی {category_url}'
            context['title'] = f'تمام محصولات در دسته بندی {category_url}'
            context['show_discount'] = True
            

        if '/brand/' in self.request.path:
            brnad_url = self.kwargs.get('brand_url')
            context['title_heading'] = f'برند {brnad_url}'
            context['title'] = f'تمام محصولات در برند {brnad_url}'
            context['show_discount'] = True            

        return context