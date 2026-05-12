from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import SupportCategory


class SupportView(TemplateView):
    template_name = 'support_module/support.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_support'] = SupportCategory.objects.filter(is_active=True, supports__isnull=False).prefetch_related('supports').distinct()
        return context
