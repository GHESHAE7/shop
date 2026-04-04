from django.urls import path
from .views import OrderView


app_name = 'car_module'

urlpatterns = [
    path('', OrderView.as_view(), name='order_page')
]
