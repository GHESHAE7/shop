from django.urls import path
from .views import AboutView, PrivacyPolicyView 


app_name = 'about_module'


urlpatterns = [
    path('', AboutView.as_view(), name='about_page'),
    path('privacy-policy', PrivacyPolicyView.as_view(), name='privacy_policy_page')
]