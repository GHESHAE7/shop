from django.urls import path
from .views import RegisterView, LoginView, logout_view, ProfileView

app_name = 'account_module'

urlpatterns = [
    path('register', RegisterView.as_view(), name='register_page'),
    path('login', LoginView.as_view(), name='login_page'),
    path( 'logout', logout_view, name='logout'),
    path( 'profile', ProfileView.as_view(), name='profile_page'),
]