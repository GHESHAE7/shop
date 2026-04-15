from django.urls import path
from .views import OrderView, StatusOrderView, remove_order_item, change_count_order_item, add_product_to_order


app_name = 'car_module'

urlpatterns = [
    path('', OrderView.as_view(), name='order_page'),
    path('status-order', StatusOrderView.as_view(), name='status_order_page'),
    path('remove-order-item', remove_order_item, name='remove-order-item'),
    path('change-count', change_count_order_item, name='change-count'),
    path('add-product-to-order', add_product_to_order, name='add_product_to_order'),
]
