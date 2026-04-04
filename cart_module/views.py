from django.shortcuts import render
from django.views import View
from cart_module.models import Order, OrderItem
from django.http import JsonResponse
# Create your views here.



class OrderView(View):
    def get(self, request):
        order = Order.objects.filter(is_active=True, user_id=request.user.id).prefetch_related('order_items').first()
        context = {
            'order': order
        }
        return render(request, 'cart_module/order.html', context)
    
    
    def post(self, request):
        pass