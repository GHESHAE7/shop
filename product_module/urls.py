from django.urls import path
from .views import ProductsListView


urlpatterns = [
    path('', ProductsListView.as_view(), name='products_page'),
    path('category/<category_url>', ProductsListView.as_view(), name='products_by_category'),
    path('brand/<brand_url>', ProductsListView.as_view(), name='products_by_brand'),
]