from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import RegisterFormModel, EditProfileFormModel
from .models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.crypto import get_random_string
from account_module.models import User
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
# Create your views here.



class RegisterView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {}
        return render(request, 'account_module/register.html', context)
    
    
    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        form: RegisterFormModel = RegisterFormModel(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            n_password = form.cleaned_data['password']
            new_user.set_password(n_password)
            new_user.is_active = False
            new_user.save()
            messages.success(request, 'حساب کاربری شما با موفقیت ساخته شد و ایمیلی جهت فعال شدن اکانت شما ارسال گردید')
            return redirect(reverse('account_module:login_page'))
        else:
            messages.error(request, 'کاربری با این مشخصات وجود دارد')
            return redirect(reverse('account_module:register_page'))
    
    
    
def active_account(request: HttpRequest, email_active_code: str) -> HttpResponseRedirect:
    current_user: User = User.objects.filter(email_active_code__exact=email_active_code, is_active=False).first()
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
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {}
        return render(request, 'account_module/login.html', context)  
   
    
    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        if not request.user.is_authenticated:
            username = request.POST['username']
            password = request.POST['password']     
            user: User = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'ورود شما موفقیت آمیز بود')
                return redirect(reverse('home_module:home_page'))
            else:
                messages.error(request, 'مشخصات وارد شده اشتباه یا اکانت شما فعال نمی باشد')
                return redirect(reverse('account_module:login_page'))
        messages.info(request, 'شما در حال حاظر درون اکانت خود هستید')
        return redirect(reverse('home_module:home_page'))
    
    
    
def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'شما از حساب کاربری خود خارج شده اید')
        path = request.META.get('HTTP_REFERER')
        return redirect(path)
    else:
        messages.error(request, 'شما لاگین نیستید اصلا')
        path = request.META.get('HTTP_REFERER')
        return redirect(path)
    
    
    
class ProfileView(View):
    def get(self, request: HttpResponse) -> HttpResponse | HttpResponseRedirect:
        if request.user.is_authenticated:
            user_id = request.user.id
            current_user: User = User.objects.filter(id=user_id, is_active=True).first()
            context = {
                'user': current_user
            }
            return render(request , 'account_module/profile.html', context)
        else:
            messages.error(request, 'شما وارد حساب کاربری خود نیستید ابتدا لاگین کنید')
            return redirect(reverse('account_module:login_page'))
    
    
    
class EditProfileView(View):
    def get(self, request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        if request.user.is_authenticated:
            user: User = request.user
            form: EditProfileFormModel = EditProfileFormModel(instance=user)
            context = {
                'form': form,
                'user': User.objects.filter(is_active=True, id=request.user.id).first()
            }
            return render(request, 'account_module/edit_profile.html', context)
        else:
            messages.error(request, 'شما وارد حساب کاربری خود نیستید ابتدا لاگین کنید')
            return redirect(reverse('account_module:login_page'))
            
            
    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        user: User = request.user
        form: EditProfileFormModel = EditProfileFormModel(request.POST, request.FILES ,instance=user)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            current_user: User = User.objects.filter(pk=user.id).first()
            if current_user.email == email:
                form.save()
                messages.success(request, 'تغییرات شما با موفقیت ذخیره شد')
                return redirect(reverse('account_module:profile_page'))
            else:
                dip_user: User = User.objects.filter(email__exact=email).first()
                if dip_user is not None:
                    messages.error(request, 'کاربری با این ایمیل وجود دارد ایمیل دیگری را انتخاب فرمایید')
                    return redirect(reverse('account_module:edit_profile_page'))
                else:
                    form.save()
                    messages.success(request, 'تغییرات شما با موفقیت ذخیره شد')
                    return redirect(reverse('account_module:profile_page'))
        else:
            return redirect(reverse('account_module:edit_profile_page'))
        
        

class SettingsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {}
        return render(request, 'account_module/settings.html', context)
    
    
    
class ChangePasswordView(View):
    def get(self, request) -> HttpResponse | HttpResponseRedirect:
        if request.user.is_authenticated:
            user: User = request.user
            current_user: User = User.objects.filter(pk=user.id, is_active=True).first()
            context = {
                'user': current_user,
            }
            return render(request, 'account_module/change_password.html', context)
        else:
            messages.error(request, 'برای تغییر پسوورد خود ابتدا باید وارد حساب کاربری خود شوید')
            return redirect(reverse('account_module:login_page'))
    
    
    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        user: User = request.user
        current_user: User = User.objects.filter(pk=user.id, is_active=True).first()
        current_password = request.POST.get('current_password')
        if current_user.check_password(current_password):
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')
            if new_password == confirm_new_password:
                current_user.set_password(confirm_new_password)
                current_user.save()
                messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد')
                logout(request)
                return redirect(reverse('account_module:login_page'))
            else:
                messages.error(request, 'رمز عبور با تکرار رمز عبور یکی نیستند')
                return redirect(reverse('account_module:change_password_page'))
        else:
            messages.error(request, 'رمز عبور فعلی شما درست نمی باشد')
            return redirect(reverse('account_module:change_password_page'))
        
        

class ForgetPasswordView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {}
        return render(request, 'account_module/forget_password.html', context)
    
    
    def post(self, request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        email = request.POST.get('email')
        current_user: User = User.objects.filter(email__exact=email, is_active=True).first()
        if current_user is not None:
            # ارسال ایمیل
            return render(request, 'account_module/forget_password_success.html')
        else:
            messages.error(request, 'کاربری با این مشخصات وجود ندارد')
            return redirect(reverse('account_module:forget_password_page'))
        
        
        
class ResetPasswordView(View):
    def get(self, request: HttpRequest, email_active_code: str) -> HttpResponse | HttpResponseRedirect:
        current_user:User = User.objects.filter(email_active_code__exact=email_active_code, is_active=True).first()
        if current_user is not None:
            context = {
                'user_email_active_code': current_user.email_active_code
            }
            return render(request, 'account_module/reset_password.html', context)
        else:
            messages.error(request, 'کاربری با این مشخصات وجود ندارد که رمزش عوض بشه')
            return redirect(reverse('home_module:home_page'))
            
    
    def post(self, request: HttpRequest, email_active_code: str) -> HttpResponseRedirect:
        current_user: User = User.objects.filter(email_active_code__exact=email_active_code, is_active=True).first()
        if current_user is not None:
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password == confirm_password:
                current_user.set_password(confirm_password)
                current_user.email_active_code = get_random_string(126)
                current_user.save()
                messages.success(request, 'رمز عبور شما با موفقیت بازیابی شد')
                if request.user.is_authenticated:
                    logout(request)
                    return redirect(reverse('account_module:login_page'))
                return redirect(reverse('account_module:login_page'))
            else:
                messages.warning(request, 'رمز عبور و تکرار رمز عبور یکی نیستند')
                return redirect(reverse('account_module:reset_password_page', kwargs={"email_active_code": current_user.email_active_code}))
        else:
            messages.error(request, 'کاربری با این مشخصات وجود ندارد که رمزش عوض بشه')
            return redirect(reverse('home_module:home_page'))