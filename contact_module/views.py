from django.shortcuts import render
from django.views import View
from .models import SubjectContact
# Create your views here.


class ContactView(View):
    def get(self, request):
        subjects = SubjectContact.objects.filter(is_active=True)
        context = {
            'subjects': subjects,
        }
        return render(request, 'contact_module/contact_us.html', context)
    
    
    def post(self, request):
        pass