from django.shortcuts import render
from django.views.generic.base import TemplateView



# Create your views here.


class SupportView(TemplateView):
    template_name = 'support_module/support.html'