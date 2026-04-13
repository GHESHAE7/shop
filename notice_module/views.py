from django.shortcuts import render
from django.views import View
from .models import Notice
from django.http import HttpRequest, HttpResponse
# Create your views here.



class NoticeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        notices = Notice.objects.filter(is_active=True).order_by('-created_at')
        context = {
            'notices': notices
        }
        return render(request, 'notice_module/notice.html', context)
    
    

class NoticeDetailView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        notice = Notice.objects.filter(is_active=True, pk=pk).first()
        context = {
            'notice': notice
        }
        return render(request, 'notice_module/notice_detail.html', context)