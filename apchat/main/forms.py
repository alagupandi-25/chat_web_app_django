from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegisterForm(UserCreationForm):
    phone_number = forms.CharField(max_length=10, required=True)
    class Meta:
        model = CustomUser
        fields = ('username','first_name' ,'last_name','email','phone_number', 'password1', 'password2')

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        if len(phone_number) !=10:
            raise forms.ValidationError("This phone number is not in correct format.")
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("This phone number is already in use.")
        return phone_number
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email


