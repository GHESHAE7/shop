from django.urls import path
from .views import LikeProductsView, delete_product_likes


app_name = 'products_like_module'

urlpatterns = [
    path('', LikeProductsView.as_view(), name='like_products_page'),
    path('delete', delete_product_likes, name='delete_like_products'),
]
