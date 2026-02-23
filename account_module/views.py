from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import RegisterFormModel
from .models import User
from django.db.models import Q
from django.contrib import messages
# Create your views here.



class RegisterView(View):
    def get(self, request):
        context = {}
        return render(request, 'account_module/register.html', context)
    
    def post(self, request):
        form = RegisterFormModel(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            n_password = form.cleaned_data['password']
            new_user.set_password(n_password)
            new_user.save()
            print('create')
            # messages.success(request, 'حساب کاربری شما با موفقیت ساخته شد')
            print('new_user save')
            return redirect(reverse('account_module:register_page'))
        # messages.error(request, 'کاربری با این مشخصات وجود دارد')
        print(form.errors)
        return redirect(reverse('account_module:register_page'))
            