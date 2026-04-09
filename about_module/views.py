from django.shortcuts import render
from django.views import View
from .models import About
# Create your views here.


class AboutView(View):
    def get(self, request):
        about = About.objects.filter(is_active=True).first()
        context = {
            'about': about,
        }
        return render(request, 'about_module/about.html', context)