from django.shortcuts import render
from django.views import View
from .models import About
# Create your views here.


class AboutView(View):
    def get(self, request):
        context = {}
        try: 
            about = About.objects.get(is_active=True)
            context['about'] = about
        except About.DoesNotExist:
            pass
        
        return render(request, 'about_module/about.html', context)