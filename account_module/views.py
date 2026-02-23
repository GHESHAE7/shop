from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import RegisterFormModel, EditProfileFormModel
from .models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
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
    
    

class LoginView(View):
    def get(self, request):
        context = {}
        return render(request, 'account_module/login.html', context)  
    
    def post(self, request):
        if not request.user.is_authenticated:
            username = request.POST['username']
            print(username)
            password = request.POST['password']     
            print(password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home_module:home_page'))
            else:
                print('مشخصات وارد شده اشتباه می باشد') 
                return redirect(reverse('account_module:login_page'))
        print('حساب کاربری شما لاگین است')
        return redirect(reverse('home_module:home_page'))
    
    
    
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        print('از حساب کاربری خارج شدید')
        return redirect(reverse('home_module:home_page'))
    else:
        print('شما لاگین نیستید')
        return redirect(reverse('home_module:home_page'))
    
    
    
class ProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user_id = request.user.id
            current_user = User.objects.filter(id=user_id, is_active=True).first()
            context = {
                'user': current_user
            }
            return render(request , 'account_module/profile.html', context)
    
    def post(self, request):
        pass
    
    
    
class EditProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            form = EditProfileFormModel(instance=user)
            context = {
                'form': form
            }
            return render(request, 'account_module/edit_profile.html', context)
            
    def post(self, request):
        user = request.user
        form = EditProfileFormModel(request.POST, request.FILES ,instance=user)
        if form.is_valid():
            form.save()
            print('تغییرات ذخیره شد')
            return redirect(reverse('account_module:profile_page'))
        else:
            print(form.errors)
            return redirect(reverse('account_module:edit_profile_page'))