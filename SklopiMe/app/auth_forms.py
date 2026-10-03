# Aleksandar Cvetkovic 2023/0150
import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email adresa',
        error_messages={
            'required': 'Email adresa je obavezna.',
            'invalid': 'Unesite ispravnu email adresu.',
        },
        widget=forms.EmailInput(attrs={
            'id': 'email',
            'placeholder': 'example@email.com',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        label='Šifra',
        error_messages={
            'required': 'Šifra je obavezna.',
        },
        widget=forms.PasswordInput(attrs={
            'id': 'password',
            'placeholder': 'Unesite šifru',
        }),
    )

    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': 'Pogrešan email ili šifra.',
    }


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Korisničko ime',
        max_length=150,
        error_messages={
            'required': 'Korisničko ime je obavezno.',
        },
        widget=forms.TextInput(attrs={
            'id': 'username',
            'placeholder': 'Unesite korisničko ime',
        }),
    )
    email = forms.EmailField(
        label='Email Adresa',
        error_messages={
            'required': 'Email adresa je obavezna.',
            'invalid': 'Unesite ispravnu email adresu.',
        },
        widget=forms.EmailInput(attrs={
            'id': 'email',
            'placeholder': 'example@email.com',
        }),
    )
    password1 = forms.CharField(
        label='Šifra',
        error_messages={
            'required': 'Šifra je obavezna.',
        },
        widget=forms.PasswordInput(attrs={
            'id': 'password',
            'placeholder': 'Unesite šifru',
        }),
    )
    password2 = forms.CharField(
        label='Potvrda Šifre',
        error_messages={
            'required': 'Potvrda šifre je obavezna.',
        },
        widget=forms.PasswordInput(attrs={
            'id': 'confirmPassword',
            'placeholder': 'potvrdite šifru',
        }),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def validate_password_for_user(self, user):
           pass

    error_messages = {
        **UserCreationForm.error_messages,
        'password_mismatch': 'Šifre se ne poklapaju.',
    }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Nalog sa ovom email adresom već postoji.')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('Nalog sa ovim korisčkim imenom već postoji.')
        return username

    def clean_password1(self):
        password = self.cleaned_data['password1']
        
        if not re.search(r'[a-z]', password):
            raise ValidationError('Šifra mora sadržati najmanje jedno malo slovo.')
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Šifra mora sadržati najmanje jedno veliko slovo.')
        
        if not re.search(r'[0-9]', password):
            raise ValidationError('Šifra mora sadržati najmanje jedan broj.')
        
        return password