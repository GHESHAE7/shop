from django.shortcuts import render
from django.views import View
from .models import LikesProduct
from django.db.models import Count, Max
from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from product_module.models import Product
# Create your views here.



class LikeProductsView(View):
    def get(self, request):
        # if request.user.is_authenticated:
        likes_products = LikesProduct.objects.filter(user_id=request.user.id, is_active=True).annotate(discount=Max('product__product_variant__discount')).order_by('-created_at')
        old_time = timezone.now() - timedelta(7)
        context = {
            'likes_products': likes_products,
            'count_likes': LikesProduct.objects.filter(user_id=request.user.id, is_active=True).aggregate(Count('user'))['user__count'] or 0,
            'old_time': old_time,

        }
        return render(request, 'products_like_module/products_like.html', context)
        # else:
    

    def post(self, request):
        if request.user.is_authenticated:
            product_id = request.POST['product_id']
            current_product = Product.objects.filter(pk=product_id, is_active=True).first()
            if current_product is not None:
                current_product_like = LikesProduct.objects.filter(product_id=current_product.id, is_active=True).first()
                if current_product_like is not None:
                    return JsonResponse({
                        'status': '200',
                        'message': 'this product avablail'
                    })
                    
                else:
                    new_product_like = LikesProduct(user_id=request.user.id, product_id=current_product.id)
                    new_product_like.save()
                    return JsonResponse({
                        'status': '200', 
                        'message': 'ok'
                    })
                    
            else:
                return JsonResponse({
                    'status': '404', 
                    'message': 'product not found'
                })
                
        else:
            return JsonResponse({
                'status': '200', 
                'message': 'user not login'
            })
            
            
            
            
def delete_product_likes(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            like_product_id = request.POST['like_product_id']
            current_like_products = LikesProduct.objects.filter(id=like_product_id, is_active=True).first()
            if current_like_products is not None:
                current_like_products.delete()
                return JsonResponse({
                    'status': '200',
                    'message': 'deleted'
                })
            else:
                return JsonResponse({
                    'status': '200',
                    'message': 'not found product'
                })
        else:
            return JsonResponse({
                'status': '200',
                'message': 'user not login'
            })