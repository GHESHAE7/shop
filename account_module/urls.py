from django.urls import path
from .views import RegisterView

app_name = 'account_module'

urlpatterns = [
    path('register', RegisterView.as_view(), name='register_page')
]