from typing import Any
from django import forms
from .models import Documentos
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User

class iniciarSesionForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(iniciarSesionForm, self).__init__(*args, **kwargs)
        for fieldname in ['username']:
            self.fields[fieldname].label = 'Rut'


class LoginForm(forms.Form):
    username = forms.CharField(label='Rut', max_length=100)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class CreaDocForm(forms.ModelForm):
    class Meta:
        model = Documentos
        fields = ['tipo_doc', 'link_doc']
    def __init__(self, *args, **kwargs):
        super(CreaDocForm, self).__init__(*args, **kwargs)
        for fieldname in ['tipo_doc']:
            self.fields[fieldname].label = 'Tipo de Post'
        for fieldname in ['link_doc']:
            self.fields[fieldname].label = 'Escribe tu Post'
        