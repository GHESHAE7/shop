from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Product, Category
from django.db.models import Max
from django.utils import timezone
from datetime import timedelta
# Create your views here.



class ProductsListView(ListView):
    template_name = 'product_module/products.html'
    model = Product
    context_object_name = 'products'
    
    
    def get_queryset(self, *args, **kwargs):
        query = super().get_queryset(*args, **kwargs)
        category_url = self.kwargs['category_url']
        if category_url is not None:
            query = query.filter(is_active=True, category__url__exact=category_url).annotate(discount=Max('product_variant__discount')).order_by('-created_at')
        else:
            query = query.filter(is_active=True).annotate(discount=Max('product_variant__discount')).order_by('-created_at')
        return query
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        old_time = timezone.now() - timedelta(7)
        categories = Category.objects.filter(is_active=True)
        context['old_time'] = old_time
        context['categories'] = categories
        return context