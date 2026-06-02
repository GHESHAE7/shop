from django.urls import path
from .views import SupportView

app_name = "support_module"


urlpatterns = [
    path("", SupportView.as_view(), name="support_page"),
]
