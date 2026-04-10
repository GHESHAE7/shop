from django.shortcuts import render
from django.views import View
from .models import Notice
# Create your views here.



class NoticeView(View):
    def get(self, request):
        notices = Notice.objects.filter(is_active=True).order_by('-created_at')
        context = {
            'notices': notices
        }
        return render(request, 'notice_module/notice.html', context)
    
    def post(self, request):
        pass