from django import forms
from .models import StudentModel


class StudentForm(forms.ModelForm):
    name = forms.CharField(label='Nome', max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Insira o nome do Estudante '
    }))
    age = forms.CharField( max_length=200, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Idade '
    }))
    address = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Endereço '
    }))
    email = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email '
    }))
    pin = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'PIN '
    }))

    mob = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mobile '
    }))
    class Meta():
        model=StudentModel
        fields=['name','age','address','email','pin','mob']

