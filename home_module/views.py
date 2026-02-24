from django.shortcuts import render
from django.views import View
from account_module.models import User
# Create your views here.


class HomeView(View):
    def get(self, request):
        context = {}
        return render(request, 'home_module/home.html', context)
    
    def post(self, request):
        pass
    
    
def header_component(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        current_user = User.objects.filter(id=user_id, is_active=True).first()
        context = {
            'user': current_user
        }
        return render(request, "component_partial/header_component.html", context)
    else:
        context = {}
        return render(request, "component_partial/header_component.html", context)


def footer_component(request):
    context = {}
    return render(request, "component_partial/footer_component.html", context)