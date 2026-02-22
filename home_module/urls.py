from django.urls import path
from .views import HomeView

app_name = "home_module"

urlpatterns = [
    path('', HomeView.as_view(), name="home_page")
]