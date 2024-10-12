from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils import timezone
from files.models import Archivo


class ArchivoForm(ModelForm):
    class Meta:
        model = Archivo
        fields = ["archivo", "directorio", "visibility"]
        widgets = {
            "archivo": forms.FileInput(attrs={"class": "form-control"}),
            "directorio": forms.TextInput(attrs={"class": "form-control"}),
            "visibility": forms.Select(attrs={"class": "form-control"}),
        }
