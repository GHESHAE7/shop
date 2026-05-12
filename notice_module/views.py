from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import Notice
from django.http import HttpRequest, HttpResponse
from django.contrib import messages



class NoticeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        notices = Notice.objects.filter(is_active=True).order_by('-created_at')
        context = {
            'notices': notices
        }
        return render(request, 'notice_module/notice.html', context)
    
    

class NoticeDetailView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            notice = Notice.objects.get(is_active=True, pk=pk)
            context = {
                'notice': notice
            }
            return render(request, 'notice_module/notice_detail.html', context)
        except Notice.DoesNotExist:
            messages.error(request, 'نوتیف مورد نظر وجود ندارد')
            return redirect(reverse('notice_module:notice_page'))
