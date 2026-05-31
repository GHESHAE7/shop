from django.urls import path
from .views import ContactView


app_name = "contact_module"

urlpatterns = [path("", ContactView.as_view(), name="contact_page")]
