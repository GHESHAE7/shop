from django.shortcuts import render
from django.views import View
# Create your views here.


class HomeView(View):
    def get(self, request):
        context = {}
        return render(request, 'home_module/home.html', context)
    
    def post(self, request):
        pass
    
    
def header_component(request):
    context = {}
    return render(request, "component_partial/header_component.html", context)


def footer_component(request):
    context = {}
    return render(request, "component_partial/footer_component.html", context)