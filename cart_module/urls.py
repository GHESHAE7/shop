from django.urls import path
from .views import (
    OrderView,
    StatusOrderView,
    remove_order_item,
    change_count_order_item,
    add_product_to_order,
    # PaymentView,
    initiate_payment,
    verify_payment,
    DiscountCodeView,
    DiscountCodeDeleteView,
)


app_name = "cart_module"

urlpatterns = [
    path("", OrderView.as_view(), name="order_page"),
    path("status-order", StatusOrderView.as_view(), name="status_order_page"),
    path("remove-order-item", remove_order_item, name="remove-order-item"),
    path("change-count", change_count_order_item, name="change-count"),
    path("add-product-to-order", add_product_to_order, name="add_product_to_order"),
    path("payment/<order_id>", initiate_payment, name="payment_order"),
    path("verify/", verify_payment, name="verify_order"),
    path("discount_code", DiscountCodeView.as_view(), name="discount_code"),
    path(
        "discount_code_delete",
        DiscountCodeDeleteView.as_view(),
        name="discount_code_delete",
    ),
]
