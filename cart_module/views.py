from django.shortcuts import render, redirect
from django.views import View
from cart_module.models import Order, OrderItem, DiscountCode, UserDiscountUsage
from django.http import JsonResponse, HttpResponse, HttpRequest
from product_module.models import ProductVariant
from django.utils.crypto import get_random_string
from account_module.models import User
from django.db.models import F, Count
from django.utils import timezone
from config import settings
from django.urls import reverse
from django.contrib import messages
from account_module.models import User


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


def initiate_payment(request: HttpRequest, order_id: int):
    if request.user.is_authenticated:
        try:
            # current_user = User.objects.get(id=request.user.id, is_active=True)
            current_user = request.user
            if not current_user.address:
                messages.warning(request, "لطفا آدرس  را در قسمت پروفایل من تکمیل کنید")
                return redirect(reverse("account_module:profile_page"))
            else:
                current_order = Order.objects.prefetch_related(
                    "order_items__product_variant"
                ).get(
                    user_id=request.user.id, id=order_id, is_active=True, status="cart"
                )
                errors_count_stock = []

                for order_item in current_order.order_items.all():
                    current_product_variant = order_item.product_variant
                    if (order_item.count > 0) and (current_product_variant.stock == 0):
                        errors_count_stock.append(
                            f"{current_product_variant.product.name} موجودی آن تمام شده است"
                        )
                        order_item.delete()
                    elif (order_item.count > 0) and (
                        order_item.count > current_product_variant.stock
                    ):
                        errors_count_stock.append(
                            f"{current_product_variant.product.name} تعدادی که انتخاب کردی بیشتر از موجودی می باشد. موجودی این محصول  {current_product_variant.stock} عدد می باشد."
                        )
                        order_item.count = current_product_variant.stock
                        order_item.save()
                try:
                    total_price = int(current_order.show_total_price())
                    discount_user = UserDiscountUsage.objects.filter(
                        order_id=current_order.id,
                        is_active=True,
                        status_usage="not_used",
                    ).first()
                    if discount_user:
                        total_price = int(
                            (
                                total_price
                                - (
                                    (total_price / 100)
                                    * int(discount_user.discount_code.percent)
                                )
                            )
                        )
                    zarinpal = settings.zarinpal
                    response = zarinpal.payments.create(
                        {
                            "amount": total_price * 10,
                            "callback_url": request.build_absolute_uri(
                                reverse("cart_module:verify_order")
                            ),
                            "description": "پرداخت سبد خرید",
                        }
                    )
                    if "data" in response and "authority" in response["data"]:
                        authority = response["data"]["authority"]
                        payment_url = zarinpal.payments.generate_payment_url(authority)
                        current_order.status = "pending"
                        current_order.save()
                        return redirect(payment_url)
                    else:
                        print("Authority not found in response.")
                except Exception as e:
                    return HttpResponse(e)

        except Exception as e:
            print("Error during payment creation:", e)
            return HttpResponse(e)
    else:
        messages.error(request, "شما برای پرداخت باید وارد حساب کاربری خود شده باشید")
        return redirect(reverse("account_module:login_page"))


def verify_payment(request):
    if request.user.is_authenticated:
        status = request.GET.get("Status")
        authority = request.GET.get("Authority")

        current_order = (
            Order.objects.filter(
                user_id=request.user.id, is_active=True, status="pending"
            )
            .prefetch_related("order_items")
            .first()
        )

        if status == "OK":
            try:
                total_price = int(current_order.show_total_price())

                discount_user = UserDiscountUsage.objects.filter(
                    order_id=current_order.id, is_active=True, status_usage="not_used"
                ).first()
                if discount_user:
                    max_uses_discount_code = (
                        UserDiscountUsage.objects.filter(
                            is_active=True,
                            discount_code=discount_user.discount_code,
                            status_usage="used",
                        ).aggregate(Count("id"))["id__count"]
                        or 0
                    )
                    print(f"max used: {max_uses_discount_code}")
                    if max_uses_discount_code < discount_user.discount_code.max_uses:
                        discount_amount_applied = (total_price / 100) * int(
                            discount_user.discount_code.percent
                        )
                        total_price = int(total_price - discount_amount_applied)
                if total_price:
                    try:
                        zarinpal = settings.zarinpal
                        response = zarinpal.verifications.verify(
                            {
                                "amount": total_price * 10,
                                "authority": authority,
                            }
                        )
                        print(f"response: {response}")
                        if response["data"]["code"] == 100:
                            ref_id = response["data"]["ref_id"]
                            card_pan = response["data"]["card_pan"]

                            current_order.rahgiri_code = ref_id
                            current_order.card_pan = card_pan
                            current_order.address = request.user.address
                            current_order.status = "paid"
                            current_order.save()

                            if (
                                discount_user
                                and max_uses_discount_code
                                < discount_user.discount_code.max_uses
                            ):
                                discount_user.discount_amount_applied = (
                                    discount_amount_applied
                                )
                                discount_user.status_usage = "used"
                                discount_user.save()

                            for order_item in current_order.order_items.all():
                                # current_product_variant = ProductVariant.objects.get(id=order_item.product_variant_id, is_active=True)
                                # current_product_variant.stock -= order_item.count
                                # current_product_variant.save()

                                ProductVariant.objects.filter(
                                    id=order_item.product_variant_id, is_active=True
                                ).update(stock=F("stock") - order_item.count)

                            context = {
                                "rahgiri_code": ref_id,
                                "number_order": current_order.id,
                            }
                            return render(
                                request, "cart_module/payment_success.html", context
                            )

                        elif response["data"]["code"] == 101:
                            print("Payment already verified.")
                            return HttpResponse("پرداخت شده بود قبلا")

                        else:
                            print(
                                "Transaction failed with code:",
                                response["data"]["code"],
                            )
                            return HttpResponse("به ارور خوردی خوشگله")

                    except Exception as e:
                        print("Payment Verification Failed:", e)
                        return HttpResponse(f"به ارور خوردی خوشگله به عنوان {e}")
                else:
                    print("No Matching Transaction Found For This Authority Code.")
                    return HttpResponse("اصن اتوریتی کدی وجود نداره عزیزم")
            except Exception as e:
                current_order.status = "cart"
                current_order.save()
                return HttpResponse(e)
        elif status == "NOK":
            print("خودت کنسل کردی عزیزم")
            current_order.status = "cart"
            current_order.save()
            context = {
                "number_order": current_order.id,
            }
            return render(request, "cart_module/payment_cancle.html", context)
        else:
            current_order.status = "cart"
            current_order.save()
            return redirect(reverse("cart_module:order_page"))
