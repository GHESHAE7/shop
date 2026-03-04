from django.urls import path
from .views import ProductsListView

app_name = 'product_module'


urlpatterns = [
    path('', ProductsListView.as_view(), name='products_page'),
    path('category/<category_url>', ProductsListView.as_view(), name='products_by_category_page'),
    path('brand/<brand_url>', ProductsListView.as_view(), name='products_by_brand_page'),
    path('discount', ProductsListView.as_view(), name='products_discount_page'),
]