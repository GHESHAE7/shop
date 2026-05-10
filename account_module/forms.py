from django import forms
from .models import User
from captcha.fields import CaptchaField

class RegisterFormModel(forms.ModelForm):
    captcha = CaptchaField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'id':'username', 'placeholder': 'farhanazizi7'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'help@example.com', 'id':'email'}),
            'password': forms.PasswordInput(attrs={'class':'form-control input-psswd', 'id':'registerPassword', 'placeholder': 'Farhan0991@'}),
        }
        
    def clean_username(self):
        data = self.cleaned_data["username"]
        if User.objects.filter(username__exact=data).exists():
            raise forms.ValidationError('کاربری با چنین مشخصات وجود دارد')
        return data
    
    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email__exact=data).exists():
            raise forms.ValidationError('کاربری با چنین مشخصات وجود دارد')
        return data
    
   

class LoginFormModel(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'username', 'placeholder': 'نام کاربری'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'password', 'placeholder': 'کلمه عبور'}))
    captcha = CaptchaField()
    
    
    
class EditProfileFormModel(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone', 'email', 'address', 'avatra']
        
        
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class':'form-control'}),
        }
        
        labels = {
            'email': 'email',
            'username': 'نام کاربری',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'phone': 'تلفن',
            'address': 'آدرس حمل و نقل',
            'avatra': 'آواتار پروفایل',
        }
