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