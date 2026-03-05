from django.shortcuts import render
from django.views import View
# Create your views here.



class LikeProductsView(View):
    def get(self, request):
        context = {}
        return render(request, 'products_like_module/products_like.html', context)
    

    def post(self, request):
        pass