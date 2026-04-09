from django.urls import path
from .views import OrderView, StatusOrderView


app_name = 'car_module'

urlpatterns = [
    path('', OrderView.as_view(), name='order_page'),
    path('status-order', StatusOrderView.as_view(), name='status_order_page')
]
