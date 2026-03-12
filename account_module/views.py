from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import RegisterFormModel, EditProfileFormModel
from .models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.crypto import get_random_string
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
            new_user.is_active = False
            new_user.save()
            # messages.success(request, 'حساب کاربری شما با موفقیت ساخته شد')
            print('new_user save')
            return redirect(reverse('account_module:login_page'))
        # messages.error(request, 'کاربری با این مشخصات وجود دارد')
        print(form.errors)
        return redirect(reverse('account_module:register_page'))
    
    
    
def active_account(request, email_active_code):
    current_user = User.objects.filter(email_active_code__exact=email_active_code, is_active=False).first()
    if current_user is not None:
        current_user.is_active = True
        current_user.email_active_code = get_random_string(126)
        current_user.save()
        print('حساب کاربر فعال شد')
        return redirect('account_module:login_page')
    else:
        print('کاربری پیدا نشد که حساب آن را فعال کنیم')
        return redirect(reverse('home_module:home_page'))
    
    

class LoginView(View):
    def get(self, request):
        context = {}
        return render(request, 'account_module/login.html', context)  
    
    def post(self, request):
        if not request.user.is_authenticated:
            username = request.POST['username']
            password = request.POST['password']     
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home_module:home_page'))
            else:
                print('مشخصات وارد شده اشتباه می باشد یا حساب کاربری شما فعال نیست')
                return redirect(reverse('account_module:login_page'))
        print('حساب کاربری شما لاگین است')
        return redirect(reverse('home_module:home_page'))
    
    
    
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        print('از حساب کاربری خارج شدید')
        path = request.META.get('HTTP_REFERER')
        return redirect(path)
    else:
        print('شما لاگین نیستید')
        path = request.META.get('HTTP_REFERER')
        return redirect(path)
    
    
    
class ProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user_id = request.user.id
            current_user = User.objects.filter(id=user_id, is_active=True).first()
            context = {
                'user': current_user
            }
            return render(request , 'account_module/profile.html', context)
        else:
            print('شما لاگین نیستید')
            return redirect(reverse('account_module:login_page'))
            
    
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
        else:
            print('شما لاگین نیستید')
            return redirect(reverse('account_module:login_page'))
            
    def post(self, request):
        user = request.user
        form = EditProfileFormModel(request.POST, request.FILES ,instance=user)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            current_user = User.objects.filter(pk=user.id).first()
            print(f'current user: {current_user}')
            if current_user.email == email:
                form.save()
                print('تغییرات ذخیره شد')
                return redirect(reverse('account_module:profile_page'))
            else:
                dip_user = User.objects.filter(email__exact=email).first()
                print(f'dip user: {dip_user}')
                if dip_user is not None:
                    print('ایمیل وجود دارد ایمیل دیگری انتخاب کنید')
                    return redirect(reverse('account_module:edit_profile_page'))
                else:
                    form.save()
                    print('تغییرات ذخیره شد')
                    return redirect(reverse('account_module:profile_page'))
        else:
            print(form.errors)
            return redirect(reverse('account_module:edit_profile_page'))
        
        

class SettingsView(View):
    def get(self, request):
        context = {}
        return render(request, 'account_module/settings.html', context)
    
    def post(self, request):
        pass
    
    
    
class ChangePasswordView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            current_user = User.objects.filter(pk=user.id, is_active=True).first()
            context = {
                'user': current_user,
            }
            return render(request, 'account_module/change_password.html', context)
        else:
            print('برای تغییر رمز باید ابتدا لاگین فرمایید')
            return redirect(reverse('account_module:login_page'))
    
    def post(self, request):
        user = request.user
        current_user = User.objects.filter(pk=user.id, is_active=True).first()
        current_password = request.POST.get('current_password')
        if current_user.check_password(current_password):
            print('پسوورد شما درست می باشذ')
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')
            if new_password == confirm_new_password:
                current_user.set_password(confirm_new_password)
                current_user.save()
                print('پسوورد کاربر تغییر  کرد')
                logout(request)
                return redirect(reverse('account_module:login_page'))
            else:
                print('پسوورد و تکرار پسوورد یکی نیستند')
                return redirect(reverse('account_module:change_password_page'))
        else:
            print('پسوورد فعلی شما درست نمی باشد')
            return redirect(reverse('account_module:change_password_page'))
        
        

class ForgetPasswordView(View):
    def get(self, request):
        context = {}
        return render(request, 'account_module/forget_password.html', context)
    
    def post(self, request):
        email = request.POST.get('email')
        current_user = User.objects.filter(email__exact=email, is_active=True).first()
        if current_user is not None:
            print('کاربر یافت شد')
            # ارسال ایمیل
            return render(request, 'account_module/forget_password_success.html')
        else:
            print('کاربری با این مشخصات یاقت نشد')
            return redirect(reverse('account_module:forget_password_page'))
        
        
        
class ResetPasswordView(View):
    def get(self, request, email_active_code):
        current_user = User.objects.filter(email_active_code__exact=email_active_code, is_active=True).first()
        if current_user is not None:
            context = {
                'user_email_active_code': current_user.email_active_code
            }
            return render(request, 'account_module/reset_password.html', context)
        else:
            print('چنین کاربری وجود ندارد')
            return redirect(reverse('home_module:home_page'))
            
    
    def post(self, request, email_active_code):
        current_user = User.objects.filter(email_active_code__exact=email_active_code, is_active=True).first()
        if current_user is not None:
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password == confirm_password:
                current_user.set_password(confirm_password)
                current_user.email_active_code = get_random_string(126)
                current_user.save()
                print('پسوورد کاربر تغییر کرد')
                if request.user.is_authenticated:
                    logout(request)
                    return redirect(reverse('account_module:login_page'))
                return redirect(reverse('account_module:login_page'))
            else:
                print('پسوورد و تکرار پسوورد یکی نیستند')
                return redirect(reverse('account_module:reset_password_page', kwargs={"email_active_code": current_user.email_active_code}))
        else:
            print('چنین کاربری وجود ندارد که ما رمزش را عوض کنیم')
            return redirect(reverse('home_module:home_page'))