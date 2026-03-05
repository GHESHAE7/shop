from django.urls import path
from .views import LikeProductsView


urlpatterns = [
    path('', LikeProductsView.as_view(), name='like_products_page'),
]
