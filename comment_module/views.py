from django.shortcuts import render
from comment_module.models import Comment

# Create your views here.



def comments_product(request, product_id):
    comments = Comment.objects.filter(is_active=True, product_id=product_id).order_by('-created_at')
    context = {
        'comments': comments
    }
    
    return render(request, 'comment_module/component_partial/single_comment.html', context)