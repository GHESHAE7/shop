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
                
                

class StatusOrderView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            user_orders: Order = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_active=True).exclude(status__in=['cart', 'paid'])
            context = {
                'orders': user_orders,
            }
            return render(request, 'cart_module/status_order.html', context)
        
        
        
def remove_order_item(request: HttpRequest) -> JsonResponse:
    if request.user.is_authenticated:
        if request.method == 'POST':
            order_item_id = request.POST.get('order_item_id') or None
            current_order_item = OrderItem.objects.filter(is_active=True, pk=order_item_id, order__user_id=request.user.id).first() or None
            if current_order_item is not None:   
                current_order_item.delete()
                return JsonResponse({
                    'icon': 'success',
                    'message': 'محصول مورد نظر با موفقیت از سبد خرید شما پاک شد'
                })
            else:
                return JsonResponse({
                    'icon': 'error',
                    'message': 'محصول مورد نظر پیدا نشد که بخوام پاکش کنم'
                })   
    else:
        return JsonResponse({
            'icon': 'error',
            'message': 'ابتدا باید وارد حساب کاربری خود شوید'
        })
        
        
        
def change_count_order_item(request: HttpRequest) -> JsonResponse:
    if request.user.is_authenticated:
        if request.method == 'POST':
            order_item_id = request.POST.get('order_item_id') or None
            current_order_item = OrderItem.objects.filter(is_active=True, pk=order_item_id, order__user_id=request.user.id).first() or None
            if current_order_item is not None:                
                new_number_count = request.POST.get('change_count') or None
                if (int(new_number_count) > current_order_item.product_variant.stock) or (int(new_number_count) <= 0):
                    return JsonResponse({
                        'icon': 'info',
                        'message': 'مقدار انتخاب شده شما بیشتر از موجودی یا کمتر از 0 می باشد'
                    })
                else:
                    current_order_item.count = new_number_count
                    current_order_item.save()
                    return JsonResponse({
                        'icon': 'success',
                        'message': 'مقدار تغییر کرد'
                    })
            else:
                return JsonResponse({
                    'icon': 'error',
                    'message': 'محصول مورد نظر پیدا نشد که مقدار آن را داخل سبد خرید شما تغیر بدم'
                })
                    
    else:
        return JsonResponse({
            'icon': 'error',
            'message': 'ابتدا باید وارد حساب کاربری خود شوید'
        })
        
        

def add_product_to_order(request: HttpRequest) -> JsonResponse:
    if request.user.is_authenticated:
        if request.method == 'POST':
            product_id = request.POST.get('product_id') or None
            order_user: Order = Order.objects.filter(is_active=True, user_id=request.user.id).first()
            if order_user is not None:
                color = request.POST.get('color_name')
                size = request.POST.get('size_name')
                current_product_variant: ProductVariant = ProductVariant.objects.filter(is_active=True, product_id=product_id, color=color, size=size).first()
                if current_product_variant is not None:
                    current_order_item = OrderItem.objects.filter(is_active=True, order_id=order_user.id, product_variant_id=current_product_variant.id).first()
                    if current_order_item is not None:
                        return JsonResponse({
                            'icon': 'info',
                            'message': 'این محصول در سبد خرید شما وجود دارد',
                        })
                    else:
                        count = request.POST.get('count')
                        if (int(count) > current_product_variant.stock) or (int(count) <= 0):
                            return JsonResponse({
                                'icon': 'warning',
                                'message': 'تعداد انتخاب شده نمی تواند بیشتر از موجودی محصول یا کوچک تر از 0 باشد'
                            })
                        else:
                            # new_order_item = OrderItem(order_id=order_user.id, product_id=product_id, product_variant_id=current_product_variant.id, count=count)
                            # new_order_item.save()
                            OrderItem.objects.create(order_id=order_user.id, product_id=product_id, product_variant_id=current_product_variant.id, count=count)
                            return JsonResponse({
                                'icon': 'success',
                                'message': 'محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد',
                            })
                else:
                    return JsonResponse({
                        'icon': 'error',
                        'message': 'محصول مورد نظر یافت نشد',
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
                            'icon': 'info',
                            'message': 'این محصول در سبد خرید شما وجود دارد',
                        })
                    else:
                        count = request.POST.get('count')
                        if (int(count) > current_product_variant.stock) or (int(count) <= 0):
                            return JsonResponse({
                                'icon': 'warning',
                                'message': 'تعداد انتخاب شده نمی تواند بیشتر از موجودی محصول یا کوچک تر از 0 باشد'
                            })
                        else:
                            new_order_item = OrderItem(order_id=new_order.id, product_id=product_id, product_variant_id=current_product_variant.id, count=count)
                            new_order_item.save()
                            return JsonResponse({
                                'icon': 'success',
                                'message': 'محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد',
                            })
                else:
                    return JsonResponse({
                        'icon': 'error',
                        'message': 'محصول مورد نظر یافت نشد',
                    })
    else:
        return JsonResponse({
            'icon': 'error',
            'message': 'ابتدل باید وارد حساب کاربری خود شوید'
        })
