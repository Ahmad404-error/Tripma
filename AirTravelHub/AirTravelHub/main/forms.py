from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Passenger
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .models import CustomUser

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

    # def save(self, commit=True):
    #     user = super(SignUpForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #     return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email

    def send_confirmation_email(self, request, user):
            subject = "Подтверждение регистрации"
            current_site = get_current_site(request)
            email_context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }
            message = render_to_string('main/registration/confirmation_email.html', email_context)
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False  # Аккаунт не активен до подтверждения
        if commit:
            user.save()
        return user
    

class PassengerForm(forms.ModelForm):
    class Meta():
        model = Passenger
        fields = ['gender', 'citizenship', 'first_name', 'last_name', 'passport_number', 'birthday']