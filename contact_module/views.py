from django.shortcuts import render
from django.views import View
# Create your views here.


class ContactView(View):
    def get(self, request):
        context = {}
        return render(request, 'contact_module/contact_us.html', context)
    
    
    def post(self, request):
        pass