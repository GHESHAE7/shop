from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product, Category, Brand, ProductVariant
from django.db.models import Max, Min, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
from comment_module.models import Comment
from django.db.models import Count
from django.http import JsonResponse, HttpRequest
# Create your views here.



class ProductsListView(ListView):
    template_name = 'product_module/products.html'
    model = Product
    context_object_name = 'products'
    
    
    def get_queryset(self, *args, **kwargs):
        query = super().get_queryset(*args, **kwargs)
        query = query.filter(is_active=True).annotate(discount=Max('product_variant__discount'), rating=Avg('comments__rating'), sales_count=Sum('product_variant__sales_count')).order_by('-created_at')
        category_url = self.kwargs.get('category_url') or None
        brand_url = self.kwargs.get('brand_url') or None
        brnads = self.request.GET.getlist('brand')
        categories = self.request.GET.getlist('category')
        rating = self.request.GET.get('rating')
        discounted = self.request.GET.get('discounted')
        max_price = self.request.GET.get('max_price') or 0
        min_price = self.request.GET.get('min_price') or 0
        order_by = self.request.GET.get('order_by') or None
        search_products = self.request.GET.get('search') or None
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
        if rating:
            query = query.filter(rating__lte=rating)
        if search_products:
            print(f'search param: {search_products}')
            query = query.filter(Q(name__icontains=search_products) | Q(category__name__icontains=search_products) | Q(category__url__icontains=search_products) | Q(brand__name__icontains=search_products) |  Q(brand__url__icontains=search_products) | 
                Q(slug__icontains=search_products) | Q(product_variant__color__icontains=search_products)
            )
        if self.request.path.endswith('/discount'):
            query = query.filter(product_variant__discount__gt=0)
        if order_by:
            if order_by == 'جدیدترین':
                query = query.order_by('-created_at')
            elif order_by == 'قدیمی ترین':
                query = query.order_by('created_at') 
            elif order_by == 'بیشترین قیمت':
                query = query.order_by('-price')          
            elif order_by == 'کمترین قیمت':
                query = query.order_by('price')       
            elif order_by == 'تخفیف دار':
                query = query.filter(product_variant__discount__isnull=False)
            elif order_by == 'بالاترین امتیاز':
                query = query.filter(rating__isnull=False).order_by('-rating')
            elif order_by == 'کم ترین امتیاز':
                query = query.filter(rating__isnull=False).order_by('rating')
            elif order_by == 'پرفروش ترین':
                query = query.order_by('-sales_count')
            elif order_by == 'کم فروش ترین':
                query = query.order_by('sales_count')
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
        context['checked_ratings'] = self.request.GET.get('rating')
        context['checked_discounted'] = self.request.GET.get('discounted')
        context['order_by'] = self.request.GET.get('order_by') or None
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
            
            
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
            context['title_heading'] = f'جستجو برای {search}'
            context['title'] = f'{search}'
            context['show_discount'] = True           

        return context
    
    
    
class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product
    context_object_name = 'product'
    
    def get_queryset(self, *args, **kwargs):
        query = super().get_queryset(*args, **kwargs)
        query = query.filter(is_active=True).prefetch_related('product_images').annotate(discount=Max('product_variant__discount'))
        return query
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attributes = ProductVariant.objects.filter(is_active=True, product=self.object).order_by('size')
        attr_colors = defaultdict(set)
        attr_sizes = defaultdict(set)
        for item in attributes:
            attr_colors['color'].add(item.color)
            attr_sizes['size'].add(item.size)
        context['colors'] = {key: list(values) for key, values in attr_colors.items()}
        context['sizes'] = {key: list(values) for key, values in attr_sizes.items()}
        context['stock'] = Product.objects.filter(id=self.object.id, is_active=True).aggregate(Sum('product_variant__stock'))['product_variant__stock__sum'] or 0
        context['count_comments'] = Comment.objects.filter(is_active=True, product=self.object).aggregate(Count('id'))['id__count'] or 0
        context['rating'] = f"{Comment.objects.filter(is_active=True, product=self.object).aggregate(Avg('rating'))['rating__avg'] or 0:.2f}"
        return context
    
    
    
def stock_color_size(request: HttpRequest) -> JsonResponse:
    try:
        color = request.POST.get('color_name')
        size = request.POST.get('size_name')
        product_id = request.POST.get('product_id')
        get_product_variant: ProductVariant = ProductVariant.objects.get(is_active=True, color__exact=color, size__exact=size, product_id=product_id).values('stock')
        return JsonResponse({
            'color': color,
            'size': size,
            'stock': get_product_variant['stock'],
        })
    except ProductVariant.DoesNotExist:
        return JsonResponse({
            'message': 'چنین محصولی وجود ندارد'
        })
