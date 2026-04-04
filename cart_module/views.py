from django.shortcuts import render
from django.views import View
from cart_module.models import Order, OrderItem
from django.http import JsonResponse, HttpResponse
# Create your views here.



class OrderView(View):
    def get(self, request):
        order = Order.objects.filter(is_active=True, user_id=request.user.id).prefetch_related('order_items').first()
        context = {
            'order': order
        }
        return render(request, 'cart_module/order.html', context)
    
    
    def post(self, request):
        order_item_id = request.POST.get('order_item_id') or None
        if order_item_id is not None:                
            current_order_item = OrderItem.objects.filter(is_active=True, pk=order_item_id).first() or None
            new_number_count = request.POST.get('change_count') or None
            if new_number_count is not None:
                if (int(new_number_count) > current_order_item.product_variant.stock) or (int(new_number_count) <= 0):
                    return JsonResponse({
                        'status': 200,
                        'message': 'نمیتونی بزرگ تر موجودی و کوچک تر از موجودی انتخاب کنی'
                    })
                else:
                    current_order_item.count = new_number_count
                    current_order_item.save()
                    return HttpResponse('مقدار تغییر کرد')
            else:
                if current_order_item is not None:
                    current_order_item.delete()
                    return JsonResponse({
                        'status': 200,
                        'message': f'deleted order item by id {order_item_id}',
                        'delete': True
                    })
                else:
                    return JsonResponse({
                        'status': 200,
                        'message': f'Not found order item by id {order_item_id}',
                        'delete': False
                    })