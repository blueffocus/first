from django import forms
from datetime import timedelta
from .models import *
def now():
    now = datetime.datetime.now()
    return now

class FormularioContacto(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Dirección Email'}))
    socio = forms.IntegerField(label="NºSocio", widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Nº de Socio'}), max_value=99999,
                              min_value=0)
    dni = forms.CharField(label="DNI", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'DNI'}), max_length=9, min_length=9)
    sel = Carrera.objects.order_by('fecha').filter(fecha__gt=now() + timedelta(days=1))
    evento = forms.ModelChoiceField(queryset=sel, empty_label='Selecciona un evento', widget=forms.Select(attrs={'class': 'form-control','placeholder':'empty_label'}), label="Carrera")
    confirmar_evento = forms.ModelChoiceField(queryset=sel, empty_label='Confirma el evento', widget=forms.Select(attrs={'class':'form-control','placeholder':'empty_label'}), label= "Confirmacion")
    comentario = forms.CharField(label="Comentario", widget=forms.Textarea(attrs={'class':'form-control','placeholder': 'Introduce comentario','cols':30,'rows':5,'style':'resize:none;'}), max_length=99999)

class FormularioContacta(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Dirección Email'}))
    asunto = forms.CharField(label="Asunto", widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Asunto'}), max_length=100,
                              min_length=3)
    nombre = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Nombre y Apellidos'}), max_length=50,
                              min_length=3)
    comentario = forms.CharField(label="Comentario", widget=forms.Textarea(attrs={'class':'form-control','placeholder': 'Introduce comentario','cols':30,'rows':5,'style':'resize:none;'}), max_length=99999)


class FormularioResultados(forms.Form):
    choices=[]
    anios = list(range(2004,now().year+1))
    for a in anios[::-1]:
        choices = choices+[(str((a.numerator)),str((a.numerator)))]
    sel = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={'class':'form-control','placeholder':'empty_label','name':'sel'}))


class FormularioCalendario2(forms.Form):
    choices=[]
    anios = list(range(2016,now().year+1))
    for a in anios[::-1]:
        choices = choices+[(str((a.numerator)),str((a.numerator)))]
    sel = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={'class':'form-control','placeholder':'empty_label','name':'sel'}))


class FormularioComentario(forms.Form):
    comentario = forms.CharField(label="Comentario", widget=forms.Textarea(attrs={'class':'form-control','placeholder': 'Introduce comentario','cols':30,'rows':2,'style':'resize:none;'}), max_length=99999, required=False)


