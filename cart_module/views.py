from django.shortcuts import render
from django.views import View
from cart_module.models import Order, OrderItem
from django.http import JsonResponse, HttpResponse
from product_module.models import Product, ProductVariant
from django.http import HttpRequest, HttpResponse
# Create your views here.



class OrderView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        order: Order = Order.objects.filter(is_active=True, user_id=request.user.id, status__in=['cart', 'paid']).prefetch_related('order_items').first()
        context = {
            'order': order
        }
        return render(request, 'cart_module/order.html', context)
    
    
    def post(self, request: HttpRequest):
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
                    

        product_id = request.POST.get('product_id') or None
        if product_id is not None:
            if request.user.is_authenticated:
                order_user = Order.objects.filter(is_active=True, user_id=request.user.id).first()
                if order_user is not None:
                    color = request.POST.get('color_name')
                    size = request.POST.get('size_name')
                    current_product_variant = ProductVariant.objects.filter(is_active=True, product_id=product_id, color=color, size=size).first()
                    if current_product_variant is not None:
                        current_order_item = OrderItem.objects.filter(is_active=True, order_id=order_user.id, product_variant_id=current_product_variant.id).first()
                        if current_order_item is not None:
                            return JsonResponse({
                                'status': 200,
                                'message': 'this product is exists',
                            })
                        else:
                            count = request.POST.get('count')
                            if (int(count) > current_product_variant.stock) or (int(count) <= 0):
                                return JsonResponse({
                                    'status': 200,
                                    'message': 'count gt is stock or count lte 0'
                                })
                            else:
                                new_order_item = OrderItem(order_id=order_user.id, product_id=product_id, product_variant_id=current_product_variant.id, count=count)
                                new_order_item.save()
                                return JsonResponse({
                                    'status': 200,
                                    'message': 'added product in order',
                                })
                    else:
                        return JsonResponse({
                            'status': 200,
                            'message': 'not found product',
                        })
                else:
                    new_order = Order(user_id=request.user.id,)
                    new_order.save()
                    color = request.POST.get('color_name')
                    size = request.POST.get('size_name')
                    current_product_variant = ProductVariant.objects.filter(is_active=True, product_id=product_id, color=color, size=size).first()
                    if current_product_variant is not None:
                        current_order_item = OrderItem.objects.filter(is_active=True, order_id=new_order.id, product_variant_id=current_product_variant.id).first()
                        if current_order_item is not None:
                            return JsonResponse({
                                'status': 200,
                                'message': 'this product is exists',
                            })
                        else:
                            count = request.POST.get('count')
                            if (int(count) > current_product_variant.stock) or (int(count) <= 0):
                                return JsonResponse({
                                    'status': 200,
                                    'message': 'count gt is stock or count lte 0'
                                })
                            else:
                                new_order_item = OrderItem(order_id=new_order.id, product_id=product_id, product_variant_id=current_product_variant.id, count=count)
                                new_order_item.save()
                                return JsonResponse({
                                    'status': 200,
                                    'message': 'first created order for you and added this product in order_item',
                                })
                    else:
                        return JsonResponse({
                            'status': 200,
                            'message': 'not found product',
                        }) 
            else:
                return JsonResponse({
                    'status': 200,
                    'message': 'user not login',
                })
                
                

class StatusOrderView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            user_orders: Order = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_active=True).exclude(status__in=['cart', 'paid'])
            context = {
                'orders': user_orders,
            }
            return render(request, 'cart_module/status_order.html', context)