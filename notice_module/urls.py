from django.urls import path
from .views import NoticeView

app_name = 'notice_module'

urlpatterns = [
    path('', NoticeView.as_view(), name='notice_page'),
]