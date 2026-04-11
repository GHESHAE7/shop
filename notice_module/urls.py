from django.urls import path
from .views import NoticeView, NoticeDetailView

app_name = 'notice_module'

urlpatterns = [
    path('', NoticeView.as_view(), name='notice_page'),
    path('<int:pk>', NoticeDetailView.as_view(), name='notice_detail_page'),
]