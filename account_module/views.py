from django.shortcuts import render
from django.views import View
# Create your views here.



class RegisterView(View):
    def get(self, request):
        context = {}
        return render(request, 'account_module/register.html', context)
    
    def post(self, request):
        pass