from django.shortcuts import render
from django.views import View
from .models import LikesProduct
from django.db.models import Count, Max, Avg
from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse, HttpRequest, HttpResponse
from product_module.models import Product


class LikeProductsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        likes_products: LikesProduct = (
            LikesProduct.objects.filter(user_id=request.user.id, is_active=True)
            .annotate(
                discount=Max("product__product_variant__discount"),
                rating=Avg("product__comments__rating"),
            )
            .order_by("-created_at")
        )
        old_time = timezone.now() - timedelta(7)
        context = {
            "likes_products": likes_products,
            "count_likes": LikesProduct.objects.filter(
                user_id=request.user.id, is_active=True
            ).aggregate(Count("user"))["user__count"]
            or 0,
            "old_time": old_time,
        }
        return render(request, "products_like_module/products_like.html", context)

    def post(self, request: HttpRequest) -> JsonResponse:
        if request.user.is_authenticated:
            try:
                product_id = request.POST["product_id"]
                current_product: Product = Product.objects.get(
                    pk=product_id, is_active=True
                )
                current_product_like: LikesProduct = LikesProduct.objects.get(
                    product_id=current_product.id, is_active=True
                )
                if current_product_like is not None:
                    return JsonResponse(
                        {
                            "icon": "info",
                            "message": "این محصول از قبل در علاقه مندی های شما وجود دارد",
                        }
                    )
            except Product.DoesNotExist:
                return JsonResponse(
                    {
                        "icon": "error",
                        "message": "چنین محصولی وجود ندارد که به علاقه مندی های شما اضافه شود",
                    }
                )
            except LikesProduct.DoesNotExist:
                new_product_like = LikesProduct(
                    user_id=request.user.id, product_id=current_product.id
                )
                new_product_like.save()
                return JsonResponse(
                    {
                        "icon": "success",
                        "message": "این محصول به علاقه مندی های شما اضافه شد",
                    }
                )

        else:
            return JsonResponse(
                {
                    "icon": "error",
                    "message": "برای افزودن به علاقه مندی ها ابتدا باید وارد حساب کاربری خود شوید",
                }
            )


def delete_product_likes(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                like_product_id = request.POST["like_product_id"]
                current_like_products = LikesProduct.objects.get(
                    id=like_product_id, is_active=True
                )
                current_like_products.delete()
                return JsonResponse(
                    {
                        "icon": "success",
                        "message": "محصول مورد نظر با موفقیت از علاقه مندی ها پاک شد",
                    }
                )
            except LikesProduct.DoesNotExist:
                return JsonResponse(
                    {
                        "icon": "200",
                        "message": "چنین محصولی وجود ندارد که از علاقه مندی ها پاک شود",
                    }
                )
        else:
            return JsonResponse(
                {"icon": "200", "message": "ابتدا باید وارد حساب کاربری خود شوید"}
            )
