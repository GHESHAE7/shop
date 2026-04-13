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
        new_contact: ContactUs = ContactUs(name=full_name, email=email, subject=subject, message=message)
        new_contact.save()
        return JsonResponse({
            'status': '200', 
            'message': 'save to database',
        })