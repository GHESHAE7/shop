from django.shortcuts import render
from django.views import View
from cart_module.models import Order, OrderItem, DiscountCode, UserDiscountUsage
from django.http import JsonResponse, HttpResponse, HttpRequest
from product_module.models import ProductVariant
from django.utils.crypto import get_random_string
from account_module.models import User
from django.db.models import F, Count
from django.utils import timezone


class OrderView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {}
        try:
            order: Order = (
                Order.objects.prefetch_related("order_items")
                .prefetch_related("discounts_applied")
                .get(is_active=True, user_id=request.user.id, status__in=["cart"])
            )
            context["order"] = order
            return render(request, "cart_module/order.html", context)
        except Order.DoesNotExist:
            return render(request, "cart_module/order.html", context)


class StatusOrderView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        user_orders: Order = (
            Order.objects.order_by("-created_at")
            .filter(user_id=request.user.id, is_active=True)
            .exclude(status__in=["cart"])
        )
        context = {
            "orders": user_orders,
        }
        return render(request, "cart_module/status_order.html", context)


def remove_order_item(request: HttpRequest) -> JsonResponse:
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                order_item_id = request.POST.get("order_item_id") or None
                current_order_item = OrderItem.objects.get(
                    is_active=True,
                    pk=order_item_id,
                    order__user_id=request.user.id,
                    order__status__in=["cart"],
                )
                current_order_item.delete()
                return JsonResponse(
                    {
                        "icon": "success",
                        "message": "محصول مورد نظر با موفقیت از سبد خرید شما پاک شد",
                    }
                )
            except OrderItem.DoesNotExist:
                return JsonResponse(
                    {
                        "icon": "error",
                        "message": "محصول مورد نظر پیدا نشد که بخوام پاکش کنم",
                    }
                )
    else:
        return JsonResponse(
            {"icon": "error", "message": "ابتدا باید وارد حساب کاربری خود شوید"}
        )


def change_count_order_item(request: HttpRequest) -> JsonResponse:
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                order_item_id = request.POST.get("order_item_id") or None
                current_order_item = OrderItem.objects.get(
                    is_active=True,
                    pk=order_item_id,
                    order__user_id=request.user.id,
                    order__status__in=["cart"],
                )
                new_number_count = request.POST.get("change_count") or None
                if (
                    int(new_number_count) > current_order_item.product_variant.stock
                ) or (int(new_number_count) <= 0):
                    return JsonResponse(
                        {
                            "icon": "info",
                            "message": "مقدار انتخاب شده شما بیشتر از موجودی یا کمتر از 0 می باشد",
                        }
                    )
                else:
                    current_order_item.count = new_number_count
                    current_order_item.save()
                    return JsonResponse(
                        {"icon": "success", "message": "مقدار تغییر کرد"}
                    )
            except OrderItem.DoesNotExist:
                return JsonResponse(
                    {
                        "icon": "error",
                        "message": "محصول مورد نظر پیدا نشد که مقدار آن را داخل سبد خرید شما تغیر بدم",
                    }
                )
    else:
        return JsonResponse(
            {"icon": "error", "message": "ابتدا باید وارد حساب کاربری خود شوید"}
        )


def add_product_to_order(request: HttpRequest) -> JsonResponse:
    if request.user.is_authenticated:
        if request.method == "POST":
            product_id = request.POST.get("product_id") or None
            try:
                order_user: Order = Order.objects.get(
                    is_active=True, user_id=request.user.id, status="cart"
                )
                color = request.POST.get("color_name")
                size = request.POST.get("size_name")
                try:
                    current_product_variant: ProductVariant = (
                        ProductVariant.objects.get(
                            is_active=True,
                            product_id=product_id,
                            color=color,
                            size=size,
                        )
                    )
                    current_order_item = OrderItem.objects.get(
                        is_active=True,
                        order_id=order_user.id,
                        product_variant_id=current_product_variant.id,
                    )
                    return JsonResponse(
                        {
                            "icon": "info",
                            "message": "این محصول در سبد خرید شما وجود دارد",
                        }
                    )
                except ProductVariant.DoesNotExist:
                    return JsonResponse(
                        {
                            "icon": "error",
                            "message": "محصول مورد نظر یافت نشد",
                        }
                    )
                except OrderItem.DoesNotExist:
                    count = request.POST.get("count")
                    if (int(count) > current_product_variant.stock) or (
                        int(count) <= 0
                    ):
                        return JsonResponse(
                            {
                                "icon": "warning",
                                "message": "تعداد انتخاب شده نمی تواند بیشتر از موجودی محصول یا کوچک تر از 0 باشد",
                            }
                        )
                    else:
                        OrderItem.objects.create(
                            order_id=order_user.id,
                            product_id=product_id,
                            product_variant_id=current_product_variant.id,
                            count=count,
                        )
                        return JsonResponse(
                            {
                                "icon": "success",
                                "message": "محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد",
                            }
                        )
            except Order.DoesNotExist:
                new_order = Order(user_id=request.user.id, status="cart")
                new_order.save()
                color = request.POST.get("color_name")
                size = request.POST.get("size_name")
                try:
                    current_product_variant = ProductVariant.objects.get(
                        is_active=True, product_id=product_id, color=color, size=size
                    )
                    current_order_item = OrderItem.objects.get(
                        is_active=True,
                        order_id=new_order.id,
                        product_variant_id=current_product_variant.id,
                    )
                    return JsonResponse(
                        {
                            "icon": "info",
                            "message": "این محصول در سبد خرید شما وجود دارد",
                        }
                    )
                except ProductVariant.DoesNotExist:
                    return JsonResponse(
                        {
                            "icon": "error",
                            "message": "محصول مورد نظر یافت نشد",
                        }
                    )
                except OrderItem.DoesNotExist:
                    count = request.POST.get("count")
                    if (int(count) > current_product_variant.stock) or (
                        int(count) <= 0
                    ):
                        return JsonResponse(
                            {
                                "icon": "warning",
                                "message": "تعداد انتخاب شده نمی تواند بیشتر از موجودی محصول یا کوچک تر از 0 باشد",
                            }
                        )
                    else:
                        new_order_item = OrderItem(
                            order_id=new_order.id,
                            product_id=product_id,
                            product_variant_id=current_product_variant.id,
                            count=count,
                        )
                        new_order_item.save()
                        return JsonResponse(
                            {
                                "icon": "success",
                                "message": "محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد",
                            }
                        )
    else:
        return JsonResponse(
            {"icon": "error", "message": "ابتدل باید وارد حساب کاربری خود شوید"}
        )


class PaymentView(View):
    def get(self, request: HttpRequest, order_id: str) -> HttpResponse:
        if request.user.is_authenticated:
            order: Order = Order.objects.filter(
                is_active=True, status="cart", pk=order_id
            ).first()
            if order is not None:
                current_user: User = User.objects.filter(
                    is_active=True, pk=request.user.id
                ).first()
                if current_user.address is None or current_user.address == "":
                    return HttpResponse("plese address")
                else:
                    order_items: OrderItem = OrderItem.objects.filter(
                        is_active=True, order_id=order.id
                    ).values_list("product_variant_id", "count")
                    for pro_var_id, count in order_items:
                        ProductVariant.objects.filter(
                            is_active=True, id=pro_var_id
                        ).update(
                            stock=F("stock") - count,
                            sales_count=F("sales_count") + count,
                        )
                    order.address = current_user.address
                    order.total_price = order.show_total_price()
                    order.status = "processing"
                    order.rahgiri_code = get_random_string(75)
                    order.save()
                    return HttpResponse("sefaresh shoma sabt shod")
            else:
                return HttpResponse("order not exists")
        else:
            return HttpResponse("you not login")


class DiscountCodeView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        if request.user.is_authenticated:
            try:
                discount_code = request.POST.get("discount_code")

                current_discount_code: DiscountCode = DiscountCode.objects.get(
                    is_active=True,
                    code__exact=discount_code,
                    expires_at__gte=timezone.now(),
                )
                order_id = request.POST.get("order_id")

                count_used_discount_code: UserDiscountUsage = (
                    UserDiscountUsage.objects.filter(
                        is_active=True,
                        discount_code_id=current_discount_code.id,
                        status_usage="used",
                    ).aggregate(Count("id"))["id__count"]
                    or None
                )

                if (
                    (count_used_discount_code is not None)
                    and (current_discount_code.max_uses is not None)
                ) and (count_used_discount_code >= current_discount_code.max_uses):
                    return JsonResponse(
                        {
                            "icon": "info",
                            "message": "تعداد استفاده از کد تخفیف تمام شده است",
                        }
                    )
                else:
                    current_user_discount_usage = UserDiscountUsage.objects.filter(
                        is_active=True,
                        order_id=order_id,
                        user_id=request.user.id,
                        discount_code_id=current_discount_code.id,
                    ).first()

                    if current_user_discount_usage is not None:
                        return JsonResponse(
                            {
                                "icon": "info",
                                "message": "کد تخفیف قبلا توسط شما استفاده یا در حال حاظر اعمال گردیده است",
                            }
                        )
                    else:
                        try:
                            UserDiscountUsage.objects.create(
                                is_active=True,
                                order_id=order_id,
                                user_id=request.user.id,
                                discount_code_id=current_discount_code.id,
                            )
                            return JsonResponse(
                                {
                                    "icon": "success",
                                    "message": "کد تخفیف اعمال شد",
                                }
                            )
                        except:
                            return JsonResponse(
                                {
                                    "icon": "error",
                                    "message": "کد تخفیف قبلا توسط شما استفاده و با آن خرید شده است",
                                }
                            )
            except DiscountCode.DoesNotExist:
                return JsonResponse(
                    {
                        "icon": "error",
                        "message": "کد تخفیف وارد شده وجود ندارد یا تاریخ آن تمام شده است",
                    }
                )
        else:
            return JsonResponse(
                {
                    "icon": "error",
                    "message": "ابتدا وارد حساب کاربری خود شوید",
                }
            )


class DiscountCodeDeleteView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        if request.user.is_authenticated:
            try:
                discount_code = request.POST.get("discount_code")
                current_discount_code: DiscountCode = DiscountCode.objects.values(
                    "id"
                ).get(
                    is_active=True,
                    code__exact=discount_code,
                    expires_at__gte=timezone.now(),
                )
                order_id = request.POST.get("order_id")
                UserDiscountUsage.objects.get(
                    is_active=True,
                    order_id=order_id,
                    user_id=request.user.id,
                    status_usage="not_used",
                    discount_code_id=current_discount_code["id"],
                ).delete()
                return JsonResponse(
                    {
                        "icon": "success",
                        "message": "کد تخفیف حذف شد",
                    }
                )
            except DiscountCode.DoesNotExist:
                return JsonResponse(
                    {
                        "icon": "error",
                        "message": "کد تخفیف وارد شده وجود ندارد",
                    }
                )
        else:
            return JsonResponse(
                {
                    "icon": "error",
                    "message": "ابتدا وارد حساب کاربری خود شوید",
                }
            )
