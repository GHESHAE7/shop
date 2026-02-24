from django.urls import path
from .views import RegisterView, LoginView, logout_view, ProfileView, EditProfileView, SettingsView, ChangePasswordView

app_name = 'account_module'

urlpatterns = [
    path('register', RegisterView.as_view(), name='register_page'),
    path('login', LoginView.as_view(), name='login_page'),
    path( 'logout', logout_view, name='logout'),
    path( 'profile', ProfileView.as_view(), name='profile_page'),
    path( 'edit-profile', EditProfileView.as_view(), name='edit_profile_page'),
    path( 'settings', SettingsView.as_view(), name='settings_page'),
    path( 'change-password', ChangePasswordView.as_view(), name='change_password_page'),
]