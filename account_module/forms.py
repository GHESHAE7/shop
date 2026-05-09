from django import forms
from .models import User

class RegisterFormModel(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
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