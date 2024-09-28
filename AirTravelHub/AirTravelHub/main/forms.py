from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Passenger

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form_control',
            'placeholder': 'Username',
        })
    )
     
    email = forms.CharField(
        max_length=100,
        label="",
        widget=forms.EmailInput(attrs={
            'class': 'form_control',
            'placeholder': 'Email',
        })
    )
    
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'class': 'form_control',
            'placeholder': 'Password',
        })
    )

    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'class': 'form_control',
            'placeholder': 'Confirm your password',
        })
    )

    data_person = forms.BooleanField(
        label="I agree to the terms and conditions",
        required=True,  # Обязательный чекбокс
    )
    
    send_mes = forms.BooleanField(
        label="Send me the latest deal alerts",
        required=False,  # Необязательный чекбокс
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'data_person', 'send_mes')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class PassengerForm(forms.ModelForm):
    class Meta():
        model = Passenger
        fields = ['gender', 'citizenship', 'first_name', 'last_name', 'passport_number', 'birthday']