from django.shortcuts import render
from comment_module.models import Comment
from django.http import JsonResponse
from product_module.models import Product

# Create your views here.



def comments_product(request, product_id):
    comments = Comment.objects.filter(is_active=True, product_id=product_id).order_by('-created_at')
    context = {
        'comments': comments
    }
    
    return render(request, 'comment_module/component_partial/single_comment.html', context)



def add_commnet(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_id = request.POST.get('product_id')
            current_product = Product.objects.filter(is_active=True, id=product_id).first()
            if current_product:
                message = request.POST.get('message')
                new_comment = Comment(is_active=True, user_id=request.user.id, product_id=current_product.id, message=message)
                new_comment.save()
                return comments_product(request=request, product_id=product_id)
            else:
                return JsonResponse({
                    'status': 200,
                    'message': 'not found product'
                })
        else:
            return JsonResponse({
                'status': 200,
                'message': 'not login'
            })