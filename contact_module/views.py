from django.shortcuts import render
from django.views import View
from .models import SubjectContact, ContactUs
from django.http import JsonResponse, HttpRequest, HttpResponse
# Create your views here.


class ContactView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        subjects: SubjectContact = SubjectContact.objects.filter(is_active=True)
        context = {
            'subjects': subjects,
        }
        return render(request, 'contact_module/contact_us.html', context)
    
    
    def post(self, request: HttpRequest) -> JsonResponse:
        full_name = request.POST.get('fl_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        ContactUs.objects.create(name=full_name, email=email, subject=subject, message=message)
        return JsonResponse({
            'icon': 'success', 
            'message': 'پیام شما ثبت شد و در اسرع وقت از طریق ایمیل به شما پاسخ داده خواهد شد',
        })