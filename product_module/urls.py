from django.urls import path
from .views import ProductsListView, ProductDetailView, stock_color_size

app_name = 'product_module'


urlpatterns = [
    path('', ProductsListView.as_view(), name='products_page'),
    path('category/<category_url>', ProductsListView.as_view(), name='products_by_category_page'),
    path('brand/<brand_url>', ProductsListView.as_view(), name='products_by_brand_page'),
    path('discount', ProductsListView.as_view(), name='products_discount_page'),
    path('detail/<slug:slug>', ProductDetailView.as_view(), name='product_detail_page'),
    path('stock_by_color_size', stock_color_size, name='stock_color_size'),
]